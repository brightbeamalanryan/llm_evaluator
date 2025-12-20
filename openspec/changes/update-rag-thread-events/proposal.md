## Why
The ASCII thread report currently parses logs, which truncates content and mixes runs. We want full-fidelity transcripts generated from structured RAG events and stored as a sidecar file for reliable reporting.

## What Changes
- Capture structured RAG thread events during execution (prompts, responses, mutator, guard, calls).
- Persist events to a JSON sidecar file per run.
- Generate ASCII thread reports from the sidecar data instead of log parsing.

## Impact
- Affected specs: reporting
- Affected code: rag runner/event capture, reporting module, rag CLI report generation
