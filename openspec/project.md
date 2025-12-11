# Project Context

## Purpose
AI Security Evaluation Framework for testing the security posture of AI systems. Initial focus on RAG (Retrieval-Augmented Generation) security testing, with planned expansion to:
- LLM prompt injection and jailbreak resistance
- Model robustness and adversarial input testing
- AI API security evaluation

## Tech Stack
- **Language:** Python 3.10+
- **CLI Framework:** Click or Typer (TBD)
- **Testing:** pytest (~50% coverage target)
- **Formatting:** Black
- **Linting:** Ruff/Flake8
- **Type Checking:** mypy (recommended)

## Project Conventions

### Code Style
- Format with Black (default settings)
- Lint with Ruff or Flake8
- Follow PEP 8 naming conventions:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_SNAKE_CASE` for constants
- Type hints encouraged for public APIs

### Architecture Patterns
- CLI-first design: primary interface is command-line
- Modular evaluation plugins for different attack types
- Clear separation between:
  - Core evaluation engine
  - Attack/test modules
  - Target adapters (for different LLM providers)
  - Reporting/output formatters

### Testing Strategy
- Unit tests with pytest
- Target ~50% code coverage
- Focus testing on:
  - Core evaluation logic
  - Attack module correctness
  - Integration with LLM providers

### Git Workflow
- Feature branches for new work
- Pull requests for code review
- Descriptive commit messages
- Main branch should always be stable

## Domain Context
- **RAG Security:** Testing retrieval-augmented generation systems for data leakage, prompt injection through retrieved documents, and context manipulation
- **Prompt Injection:** Techniques where malicious inputs cause LLMs to ignore instructions or execute unintended actions
- **Jailbreaking:** Bypassing safety guardrails and content policies
- **Adversarial Testing:** Inputs designed to cause model misbehavior or unexpected outputs

## Important Constraints
- Must support both local and cloud-based LLM providers
- API keys and credentials must never be committed to the repo
- Evaluation results may contain sensitive data - handle appropriately
- Rate limiting awareness for cloud API calls

## External Dependencies
- **Cloud LLM Providers:** OpenAI, Anthropic, and others via their respective APIs
- **Local LLM Runtimes:** Ollama, vLLM, or similar for self-hosted models
- **Vector Databases:** For RAG testing (specific providers TBD)
