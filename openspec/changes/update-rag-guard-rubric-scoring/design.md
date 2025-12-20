## Context
RAG scoring currently uses detectors for severity and guard verdicts for pass/fail. This produces false negatives and low severity when the response leaks sensitive content not matched by regex patterns.

## Goals / Non-Goals
- Goals:
  - Use a guard LLM rubric to determine both pass/fail and severity (0-100).
  - Keep RAG scoring output shape stable for reports (severity score, notes).
- Non-Goals:
  - Changing non-RAG scoring pipelines.
  - Introducing new external dependencies.

## Decisions
- Decision: Guard rubric output MUST be machine-parseable and include verdict, severity score, and notes.
  - Rationale: Eliminates detector bias and makes severity reflect holistic assessment.
- Decision: Treat invalid or malformed guard output as FAIL with severity 0 and note the issue.
  - Rationale: Preserve safety and surface guard reliability issues.

## Risks / Trade-offs
- Risk: Guard model variability could introduce scoring drift.
  - Mitigation: Constrain output format and rubric, add unit tests, and log raw guard output.

## Migration Plan
- Update RAG scoring to call guard rubric and drop detector-based scoring.
- Adjust tests to use deterministic guard responses.
- Validate CLI output and summaries still populate.

## Open Questions
- None.
