## Why
RAG severity scoring currently depends on pattern-based detectors, which can miss real leaks and under-score incidents. We want the guard model to assess both pass/fail and severity using a rubric so scoring aligns with actual leakage behavior.

## What Changes
- Replace detector-based RAG pass/fail and severity scoring with guard LLM rubric scoring.
- Update the guard prompt/output format to include a numeric severity score and notes.
- Preserve RAG test expectations and integrate rubric-driven scores into summaries and logs.

## Impact
- Affected specs: rag-security
- Affected code: rag scoring, guard scorer prompt/parsing, CLI reporting, tests
