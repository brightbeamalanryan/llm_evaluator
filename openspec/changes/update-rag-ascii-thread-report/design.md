## Context
RAG runs emit detailed log lines that are difficult to interpret. The reporting module already supports JSON/HTML/PDF outputs but lacks a compact conversational transcript view tailored to RAG sessions.

## Goals / Non-Goals
- Goals:
  - Provide a per-test ASCII thread view that reads like a chat transcript.
  - Show query/response evolution with clear roles, timestamps, and iteration markers.
  - Include call events (mutator, guard scoring, HTTP) in a visually distinct, indented style.
- Non-Goals:
  - Replacing the existing JSON/HTML/PDF reports.
  - Building a GUI or browser-based viewer.

## Decisions
- Decision: Implement a new report format (e.g., `ascii`) under the reporting module, generated alongside other report formats.
  - Rationale: Aligns with existing report pipeline and config-driven output.
- Decision: Thread rendering should be “message-first,” with events indented beneath the message that triggered them.
  - Rationale: Keeps the evolution of prompts/responses legible while still exposing call details.

## Risks / Trade-offs
- Risk: Parsing logs could be brittle.
  - Mitigation: Prefer structured event capture in the RAG runner if feasible; otherwise constrain parsing to known log patterns.

## Migration Plan
- Add ASCII reporter and wire into report generation.
- Extend RAG run to provide structured events or parse logs to build threads.
- Add tests and example output.

## Open Questions
- Whether to include all HTTP calls or only RAG/mutator/guard events (defaults TBD).
