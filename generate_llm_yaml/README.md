# PolyApp LLM YAML Generator

This project generates YAML configuration files for lessons and YouTube Shorts using Pydantic models, OpenAI's Grok API, and JSON schemas. It is organized for easy extension and automation, with CI/CD in mind.

## Features
- Strict schema validation using Pydantic
- YAML output for lesson and short configurations
- Organized directory structure for schemas and outputs
- Ready for CI/CD integration (linting, type checking, and deployment)

## Directory Structure
```
generate_llm_yaml/
├── output/         # YAML output files
├── schemas/        # JSON schema files
├── generate_yaml.py
├── models.py
├── __init__.py
├── README.md
```

## Setup
1. **Clone the repo**
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -e .
   ```
4. **Set your API key:**
   Create a `.env` file in the root with:
   ```
   XAI_API_KEY=your_xai_api_key_here
   ```
5. **Run the generator:**
   ```bash
   python3 generate_llm_yaml/generate_yaml.py
   ```

## CI/CD
- Linting and type checking will be enforced on all pull requests.
- All merges to `main` will trigger a deployment pipeline (to be configured).

## Contributing
- Fork the repo and create a feature branch.
- Ensure all checks pass before submitting a PR.

---
MIT License 