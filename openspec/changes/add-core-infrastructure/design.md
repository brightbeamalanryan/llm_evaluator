## Context
This is the foundational infrastructure for the AI security evaluation framework. All security testing capabilities will build on this core.

## Goals / Non-Goals
- Goals:
  - Provide consistent LLM provider interface
  - Enable JSON/YAML test definitions
  - Support both local and cloud LLM providers
  - Generate actionable reports
- Non-Goals:
  - GUI interface (CLI-first)
  - Real-time monitoring (batch evaluation only)

## Decisions
- **CLI Framework:** Typer (modern, type-hint based, good DX)
- **Async:** Use asyncio for concurrent test execution
- **Config:** YAML for human-readable configuration
- **Test Schema:** JSON for test definitions (tooling-friendly)

## Package Structure
```
src/eval_fw/
├── __init__.py
├── cli/
│   ├── __init__.py
│   └── main.py
├── providers/
│   ├── __init__.py
│   ├── base.py
│   ├── openai.py
│   ├── anthropic.py
│   └── ollama.py
├── engine/
│   ├── __init__.py
│   ├── loader.py
│   ├── runner.py
│   └── scorer.py
├── config/
│   ├── __init__.py
│   └── settings.py
└── reporting/
    ├── __init__.py
    ├── json_report.py
    ├── html_report.py
    └── pdf_report.py
```

## Risks / Trade-offs
- Async complexity vs simpler sync execution → Async needed for rate-limited APIs
- Multiple report formats vs single format → Users need different outputs for different audiences
