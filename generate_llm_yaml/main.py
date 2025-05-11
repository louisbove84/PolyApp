import json
import os
from pathlib import Path
from typing import cast

import yaml
from dotenv import load_dotenv
from openai import OpenAI

from generate_llm_yaml.models import (
    AnimationDict,
    ContentDict,
    LessonConfig,
    LessonDict,
    ShortConfig,
)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the prompt template
PROMPT_TEMPLATE = """
Generate a YAML configuration for an educational video about {topic}.
The video should be {duration} minutes long and targeted at {difficulty} level.

Please provide:
1. A lesson configuration with:
   - Title
   - Topic
   - Duration
   - Difficulty level
   - Content sections (introduction, explanation, example)

2. A YouTube Shorts configuration with:
   - A script for a 60-second video
   - List of animations to use

Use the following format:
```yaml
lesson:
  title: "string"
  topic: "Physics|Cryptocurrency|Coding"
  duration: 15|30|45|60
  difficulty: "Beginner|Intermediate|Advanced"
content:
  introduction: "string"
  explanation: "string"
  example: "string"
script: "string"
animations:
  - description: "Mass to Light|Equation Reveal|Energy Burst"
    duration: 5|10|15
    color: "Blue|Yellow|White"
```
"""


def generate_config(
    topic: str, duration: int, difficulty: str
) -> dict[str, LessonDict | ContentDict | str | list[AnimationDict]]:
    """Generate configuration using OpenAI API."""
    prompt = PROMPT_TEMPLATE.format(
        topic=topic, duration=duration, difficulty=difficulty
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

    # Extract YAML content from response
    content = response.choices[0].message.content
    if content is None:
        raise ValueError("Empty response from OpenAI API")
    yaml_content = content.split("```yaml")[1].split("```")[0].strip()

    # Parse YAML
    return cast(
        dict[str, LessonDict | ContentDict | str | list[AnimationDict]],
        yaml.safe_load(yaml_content),
    )


def validate_config(
    config: dict[str, LessonDict | ContentDict | str | list[AnimationDict]],
) -> tuple[LessonConfig, ShortConfig]:
    """Validate configuration using Pydantic models."""
    lesson_config = LessonConfig(
        lesson=config["lesson"],  # type: ignore
        content=config["content"],  # type: ignore
    )
    short_config = ShortConfig(
        script=config["script"],  # type: ignore
        animations=config["animations"],  # type: ignore
    )
    return lesson_config, short_config


def save_config(
    config: dict[str, LessonDict | ContentDict | str | list[AnimationDict]],
    output_dir: str,
) -> None:
    """Save configuration to YAML file."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate filename based on lesson title
    title = config["lesson"]["title"].lower().replace(" ", "_")  # type: ignore
    filename = f"{title}_config.yaml"

    # Save to YAML
    with open(output_path / filename, "w") as f:
        yaml.dump(config, f, default_flow_style=False)

    # Save to JSON for backup
    with open(output_path / f"{title}_config.json", "w") as f:
        json.dump(config, f, indent=2)


def main() -> None:
    """Main function to generate and save configuration."""
    # Example usage
    config = generate_config(topic="Physics", duration=15, difficulty="Beginner")

    # Validate configuration
    lesson_config, short_config = validate_config(config)

    # Save configuration
    save_config(config, "output")


if __name__ == "__main__":
    main()
