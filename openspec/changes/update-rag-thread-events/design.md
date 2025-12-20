## Context
RAG thread visualization currently parses log output, which is lossy and can include mixed runs. We need structured, full-text events captured during execution.

## Goals / Non-Goals
- Goals:
  - Capture full prompt/response content for each RAG iteration.
  - Store a per-run JSON sidecar containing thread events.
  - Generate ASCII thread report from sidecar data, not logs.
- Non-Goals:
  - Changing non-RAG reporting pipelines.
  - Reducing content size (store all data as requested).

## Decisions
- Decision: Record events in memory during `rag-run` and write a sidecar JSON file alongside reports.
  - Rationale: Avoids log truncation and mixed-run issues.
- Decision: ASCII report renderer will accept sidecar data directly when available.
  - Rationale: Consistent, full-fidelity rendering.

## Risks / Trade-offs
- Risk: Large outputs for long runs.
  - Mitigation: Keep sidecar files separate and explicitly configured in report output directory.

## Migration Plan
- Add event capture in RAG runner/CLI.
- Add sidecar JSON schema and writer.
- Update ASCII reporter to consume sidecar data.
- Update tests and documentation.

## Open Questions
- None.
