## Context
Guard models add a layer of defense but introduce their own failure modes. This evaluation framework tests both the guard's effectiveness and its own vulnerabilities.

## Goals / Non-Goals
- Goals:
  - Measure guard model accuracy
  - Detect guard-specific vulnerabilities
  - Score guard reliability
- Non-Goals:
  - Guard model training
  - Real-time guard deployment

## Decisions
- **Pipeline:** Target model → Guard model → Meta-evaluator
- **Metrics:** Precision, recall, F1 for guard classifications
- **Ground Truth:** Human-labeled test cases for accuracy measurement

## Guard Evaluation Flow
```
Input → Target Model → Output
                ↓
          Guard Model → Classification
                ↓
         Meta-Evaluator → Analysis
                ↓
         Metrics: FP, FN, Reliability Score
```

## Guard Failure Modes
1. **Hallucinated Rules:** Guard invents policies
2. **Overly Strict:** High false positive rate
3. **Bypass Vulnerable:** Specific patterns evade guard
4. **Inconsistent:** Same input, different classifications
