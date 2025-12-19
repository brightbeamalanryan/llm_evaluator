## ADDED Requirements
### Requirement: Rotating log output
The system SHALL write plain-text logs to a single file within the configured `log_dir`, and SHALL rotate the log file hourly.

#### Scenario: Hourly rotation in default log directory
- **WHEN** a test run initializes logging with the default configuration
- **THEN** a plain-text log file is created under `log_dir`
- **AND** the log file rotates on an hourly schedule

### Requirement: Unified logging for RAG suite
The system SHALL emit RAG suite execution logs to the same rotating log file used by standard evaluation runs.

#### Scenario: RAG run emits to shared log file
- **WHEN** the RAG test runner executes a suite
- **THEN** its log events are written to the shared rotating log file
