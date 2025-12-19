## Why
Canary tokens provide a simple but highly effective method for detecting catastrophic prompt leakage. By injecting invisible markers into system prompts, any appearance in output indicates a critical security failure. Few organizations implement this despite its effectiveness.

## What Changes
- Zero-width unicode canary injection
- Multiple canary type support (unicode, semantic, structural)
- Automatic canary detection in outputs
- Catastrophic leak alerting
- Canary management CLI commands

## Impact
- Affected specs: core (depends on)
- Affected code: `src/eval_fw/suites/canary_detection/`
