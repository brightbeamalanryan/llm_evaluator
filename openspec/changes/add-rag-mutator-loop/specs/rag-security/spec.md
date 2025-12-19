## ADDED Requirements

### Requirement: Iterative Prompt Mutation
The system SHALL optionally refine RAG attack prompts by invoking a mutator model for a configurable number of iterations, using prior prompt and response history to guide each mutation.

#### Scenario: Iterative refinement enabled
- **GIVEN** mutator settings are enabled with max iterations > 0
- **WHEN** a RAG test case is executed
- **THEN** the runner produces mutated prompts sequentially using the previous prompt/response history

### Requirement: Plateau-Based Stopping
The system SHALL stop mutating prompts when the RAG scoring module indicates negligible improvement over a configurable plateau window.

#### Scenario: Plateau reached
- **GIVEN** plateau tolerance and window are configured
- **WHEN** the score improvement stays below the tolerance for the window
- **THEN** the mutation loop stops before max iterations
