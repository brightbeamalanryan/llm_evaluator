## Why
Guard models (secondary LLMs that validate primary model outputs) are increasingly common but rarely evaluated systematically. Organizations need metrics for guard model accuracy, false positive/negative rates, and detection of guard-specific vulnerabilities like hallucinated rules.

## Implementation Complete

All tasks have been implemented:

### Core Infrastructure (via add-core-infrastructure)
- Target + guard model pipeline (`src/eval_fw/engine/runner.py`)
- Guard model adapter interface (`src/eval_fw/engine/scorer.py`)
- Guard response classification with Verdict enum (ALLOW/BLOCK/INVALID)

### Meta-Evaluation (`src/eval_fw/guard/meta_evaluator.py`)
- HallucinatedRuleDetector - detects guards inventing policies
- ParaphrasingDetector - detects guards rewriting instead of classifying
- StructuralLeakageAnalyzer - detects guards leaking internal information
- MetaEvaluator - combined analysis runner

### Guard Bypass Suite (`src/eval_fw/guard/bypass.py`)
- Encoding tests (Base64, ROT13)
- Roleplay tests (character, developer mode)
- Obfuscation tests (leetspeak, spacing, typos)
- Prompt injection tests (ignore instructions, fake system prompts)
- Context manipulation tests (fictional, educational framing)

### Metrics & Scoring (`src/eval_fw/guard/metrics.py`)
- GroundTruthLabel enum (SAFE, UNSAFE, AMBIGUOUS)
- DisagreementType enum (FP, FN, TP, TN, etc.)
- GuardMetrics with precision, recall, F1, reliability score
- compute_guard_metrics() function

### Testing
- 25 unit tests in `tests/test_guard.py`
- All 54 project tests passing

## Impact
- Affected specs: core (depends on), prompt-security (shares tests)
- Affected code: `src/eval_fw/guard/` (new module)
