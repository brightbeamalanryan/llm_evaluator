## Why
Guard models (secondary LLMs that validate primary model outputs) are increasingly common but rarely evaluated systematically. Organizations need metrics for guard model accuracy, false positive/negative rates, and detection of guard-specific vulnerabilities like hallucinated rules.

## What Changes
- Target model + guard model dual testing
- Meta-evaluator for guard behavior analysis
- False positive/negative tracking
- Guard reliability scoring
- Disagreement classification
- Guard bypass testing

## Impact
- Affected specs: core (depends on), prompt-security (shares tests)
- Affected code: `src/eval_fw/suites/guard_model/`
