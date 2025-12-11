## Why
The AI security evaluation framework needs foundational infrastructure: CLI interface, LLM provider adapters, test execution engine, configuration management, and reporting base. All other capabilities depend on this core.

## What Changes
- New CLI application with Click/Typer
- LLM provider abstraction (OpenAI, Anthropic, Ollama, vLLM)
- Test definition schema (JSON/YAML)
- Test execution engine with async support
- Configuration management (YAML config files)
- Base reporting infrastructure (JSON, HTML, PDF)
- Logging and error handling patterns

## Impact
- Affected specs: None (greenfield)
- Affected code: Creates `src/eval_fw/` package structure
