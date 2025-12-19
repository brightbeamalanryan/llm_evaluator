## Why
Executive stakeholders need high-level visibility into LLM security posture without diving into technical details. A dashboard aggregating metrics from all security suites with trend visualization enables informed decision-making and demonstrates security investment value.

## What Changes
- Aggregated security metrics dashboard
- Prompt leakage rate tracking
- Guard model accuracy metrics
- RAG integrity scoring
- Trend visualization over time
- Weekly/monthly report generation
- Configurable alerting thresholds

## Impact
- Affected specs: core (depends on), all other suites (aggregates)
- Affected code: `src/eval_fw/reporting/dashboard/`
