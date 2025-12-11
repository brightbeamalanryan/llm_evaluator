## ADDED Requirements

### Requirement: Metrics Aggregation
The system SHALL aggregate security metrics from all evaluation suites.

#### Scenario: Collect suite results
- **WHEN** evaluations complete
- **THEN** metrics are stored with timestamps for trend analysis

#### Scenario: Calculate composite score
- **WHEN** user requests security score
- **THEN** the system calculates weighted composite from all suites

### Requirement: Trend Visualization
The system SHALL display security metrics trends over time.

#### Scenario: Generate trend chart
- **WHEN** user requests trend report
- **THEN** the system displays metrics over selected time period

#### Scenario: Highlight regressions
- **WHEN** metrics worsen compared to previous period
- **THEN** the chart highlights regression with severity indicator

### Requirement: Executive Report Generation
The system SHALL generate executive-friendly security reports.

#### Scenario: Generate weekly report
- **WHEN** user executes `eval-fw report --weekly`
- **THEN** the system generates a summary report with:
  - Overall security score
  - Key metrics by suite
  - Top vulnerabilities found
  - Recommended actions

#### Scenario: Generate monthly report
- **WHEN** user executes `eval-fw report --monthly`
- **THEN** the system generates a comprehensive report with trends and comparisons

### Requirement: Alerting on Thresholds
The system SHALL alert when metrics exceed configured thresholds.

#### Scenario: Critical threshold breach
- **WHEN** a metric exceeds critical threshold
- **THEN** the system sends immediate alert via configured channel

#### Scenario: Warning threshold breach
- **WHEN** a metric exceeds warning threshold
- **THEN** the system includes warning in next scheduled report
