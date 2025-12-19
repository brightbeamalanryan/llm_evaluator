## Why
Organizations need to evaluate LLM resistance to prompt injection, jailbreaking, and system prompt leakage. A structured test suite with standardized scoring enables consistent security assessment across models and deployments.

## What Changes
- Prompt leakage detection tests
- Policy paraphrasing detection
- Roleplay bypass testing
- Multi-turn conversation attack tests
- Adversarial suffix vulnerability tests
- PASS/FAIL/UNCERTAIN scoring taxonomy
- Pre-built test library covering OWASP LLM Top 10

## Impact
- Affected specs: core (depends on)
- Affected code: `src/eval_fw/suites/prompt_security/`
