## Why
Current runs do not emit structured logs, which makes troubleshooting and audit trails difficult. We need a single rotating log file that captures both standard and RAG suite activity.

## What Changes
- Add rotating, hourly log output in plain text under the configured `log_dir`.
- Route RAG suite activity through the same logging pipeline as standard runs.

## Impact
- Affected specs: logging (new capability)
- Affected code: `src/eval_fw/cli/main.py`, `src/eval_fw/rag/runner.py`, `src/eval_fw/config/settings.py`, new logging module
