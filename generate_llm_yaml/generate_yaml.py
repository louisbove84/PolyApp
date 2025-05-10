import yaml
import json
import re
from pydantic import ValidationError
from openai import OpenAI
from dotenv import load_dotenv
import os
from models import LessonConfig, ShortConfig

# Load API key
load_dotenv()
api_key = os.getenv("XAI_API_KEY")

# Initialize Grok client
client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

def load_schema(file_path):
    """Load JSON schema from a file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise ValueError(f"Failed to load schema from {file_path}: {e}")

def generate_yaml(config_model, schema_file, output_file):
    """
    Generate a YAML file using Grok and validate with Pydantic.
    
    Args:
        config_model: Pydantic model (LessonConfig or ShortConfig)
        schema_file: Path to JSON schema file
        output_file: Path to save YAML
    """
    try:
        # Load schema
        schema = load_schema(schema_file)
        
        # Construct prompt
        schema_str = json.dumps(schema, indent=2)
        prompt = f"""
Return a JSON object for a configuration with the following structure and allowed values. Select ONE value from each array of options for fields like 'title', 'script', or 'description'. For lists like 'animations', include 1-3 objects, each with ONE value per field. Return ONLY the JSON object, no additional text, markdown, or explanations.

{schema_str}

Example for lesson:
{{
  "lesson": {{
    "title": "E=MC² Basics",
    "topic": "Physics",
    "duration": 30,
    "difficulty": "Intermediate"
  }},
  "content": {{
    "introduction": "Explore a key concept.",
    "explanation": "Understand the core idea.",
    "example": "Real-world application."
  }}
}}

Example for short:
{{
  "script": "Explain E=MC² in simple terms.",
  "animations": [
    {{
      "description": "Mass to Light",
      "duration": 10,
      "color": "Blue"
    }}
  ]
}}
"""
        
        # Generate response from Grok
        response = client.chat.completions.create(
            model="grok-beta",  # Update to grok-3 when available
            messages=[
                {"role": "system", "content": "You are a precise assistant that generates JSON objects with strict adherence to provided schemas. Return ONLY the JSON object, no additional text or markdown."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        # Get raw response
        raw_content = response.choices[0].message.content
        print("Raw API response:", raw_content)
        
        # Remove markdown code blocks
        cleaned_content = re.sub(r'^```json\n|\n```$', '', raw_content, flags=re.MULTILINE).strip()
        
        # Parse JSON
        try:
            json_output = json.loads(cleaned_content)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print("Cleaned content:", cleaned_content)
            # Fallback: Try extracting JSON
            json_match = re.search(r'\{.*\}', cleaned_content, re.DOTALL)
            if json_match:
                json_output = json.loads(json_match.group(0))
            else:
                raise ValueError("No valid JSON found in response")

        # Validate with Pydantic
        config = config_model(**json_output)

        # Convert to YAML
        with open(output_file, "w") as f:
            yaml.safe_dump(config.model_dump(), f, sort_keys=False)
        print(f"Successfully generated {output_file}")

    except ValidationError as e:
        print(f"Pydantic validation error: {e}")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise

# Generate Lesson Config
generate_yaml(LessonConfig, "generate_llm_yaml/schemas/lesson_schema.json", "generate_llm_yaml/output/lesson.yaml")

# Generate Short Config
generate_yaml(ShortConfig, "generate_llm_yaml/schemas/short_schema.json", "generate_llm_yaml/output/short.yaml")