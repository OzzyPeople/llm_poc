# LLM POC

Proof of Concept project for experimenting with **LLM-powered pipelines**:  
- **GeminiClient** wrapper for Google’s Gemini models  
- **Schemas** defined with Pydantic for structured outputs  
- **Evaluation** utilities (metrics, judge) for model responses  
- **Utils** with data loaders and fixes  

## Structure
src/
├── clients/ # API clients (e.g., Gemini)
├── evaluation/ # Metrics, judge logic
├── llm_poc/ # Main entrypoint (main.py)
├── schemas/ # Pydantic schemas for outputs
└── utils/ # Helpers (loader, fixes)

## Run
```bash
poetry install
poetry run python -m llm_poc

Notes

Python 3.11+
Poetry for dependency management
.gitignore excludes notebooks, data, and envs