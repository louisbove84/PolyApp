import json
import os
import re
from pathlib import Path
from typing import TypedDict, cast

import yaml
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError

from .models import (
    AnimationDict,
    ContentDict,
    LessonConfig,
    LessonDict,
    ShortConfig,
)

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class SchemaDict(TypedDict):
    """Type for the schema dictionary."""

    lesson: LessonDict
    content: ContentDict
    script: str
    animations: list[AnimationDict]


def load_schema(file_path: str) -> SchemaDict:
    """Load schema from YAML file."""
    with open(file_path, "r") as f:
        return cast(SchemaDict, yaml.safe_load(f))


def generate_yaml(
    config_model: type[LessonConfig | ShortConfig], schema_file: str, output_file: str
) -> None:
    """Generate YAML using OpenAI and validate with Pydantic."""
    schema = load_schema(schema_file)
    prompt = (
        "You are an AI that generates JSON objects for educational video configs. "
        "Strictly follow this schema: "
        f"{json.dumps(schema)}\n"
        "Values: Select ONE value from each array of options for fields like 'title', "
        "'script', or 'description'. For lists like 'animations', include 1-3 objects, "
        "each with ONE value per field. Return ONLY the JSON object, no additional text, "
        "markdown, or explanations."
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=1000,
    )
    raw_content = response.choices[0].message.content
    if raw_content is None:
        raise ValueError("Empty response from OpenAI API")
    # Remove markdown code blocks
    cleaned_content = re.sub(
        r"^```json\n|\n```$", "", raw_content, flags=re.MULTILINE
    ).strip()
    # Parse JSON
    try:
        json_match = re.search(r"\{.*\}", cleaned_content, re.DOTALL)
        if json_match:
            json_output = json.loads(json_match.group(0))
        else:
            raise ValueError("No valid JSON found in response")
    except Exception as err:
        raise ValueError("Failed to parse JSON from response") from err
    # Validate with Pydantic
    try:
        config = config_model(**json_output)
    except ValidationError as err:
        raise ValueError(f"Validation error: {err}") from err
    # Save YAML
    with open(output_file, "w") as f:
        yaml.dump(json_output, f, default_flow_style=False)


# Generate Lesson Config
generate_yaml(
    LessonConfig,
    "generate_llm_yaml/schemas/lesson_schema.json",
    "generate_llm_yaml/output/lesson.yaml",
)
# Generate Short Config
generate_yaml(
    ShortConfig,
    "generate_llm_yaml/schemas/short_schema.json",
    "generate_llm_yaml/output/short.yaml",
)
