## Why
The RAG suite currently runs static prompts and does not use the `prompt-mutator` model described in the RAG security proposal, so iterative adversarial refinement is missing. We also need to make the `injected_doc` payload in RAG use cases explicitly part of the evaluation flow so it is not ignored.

## What Changes
- Add an iterative prompt mutation loop to the RAG runner that calls the `prompt-mutator` model with prior prompt/response history for a configurable number of iterations.
- Introduce RAG mutator settings in config (enabled flag, model name, plateau tolerance, max iterations, temperature/top_p override) and wire them into the RAG runner.
- Use the RAG scoring module to compute a plateau signal that stops mutation when gains are negligible.
- Add tests covering mutator iteration behavior and plateau-based stopping in the RAG suite.

## Impact
- Affected specs: rag-security
- Affected code: `src/eval_fw/rag/runner.py`, `src/eval_fw/rag/scoring.py`, `src/eval_fw/config/settings.py`, `src/eval_fw/cli/main.py`, `tests/test_rag.py`, `tests/test_logging.py`
