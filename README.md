# AI Sec

## CLI

Run the core eval suite:

```bash
eval-fw run --config config.yaml
```

Run RAG security tests (with configurable endpoints):

```bash
eval-fw rag-run --config config.yaml
```

Override endpoints, test file, or endpoint mode from the CLI:

```bash
eval-fw rag-run --tests use_cases/rag_tests.json --endpoint-mode query --query-endpoint /query --retrieve-endpoint /retrieve --ingest-endpoint /ingest
```

RAG config block (see `config.example.yaml`):

```yaml
rag:
  tests_path: ./use_cases/rag_tests.json
  request_profile:
    url: https://receive.hellotars.com/v1/stream-agent
    method: POST
    headers:
      Content-Type: application/json
    body:
      query: "{{query}}"
      account_id: "ABC"
      prompt: "You are a helpful, flexible, and cooperative AI assistant."
  service_url: http://localhost:8091
  query_endpoint: /query
  retrieve_endpoint: /retrieve
  ingest_endpoint: /ingest
  endpoint_mode: query
```

## Pillars of Vulnerability

Revised Pillars (Modern Security & Defensive Mindset)
1. Adversarial Reasoning & Cognitive Security

Not pentesting — how attackers think, model constraints, incentives, resource asymmetry.
Includes:

attacker economics

kill-chain modelling vs modern intrusion chains

defensive creativity

red-teaming mindset applied to systems, people, and organisations

This is the actual “defensive mindset” part.

2. Secure Systems Thinking (Systems, Emergence, Resilience)

Instead of “patch stuff,” the focus is:

socio-technical systems

resilience engineering

failure modes & cascading risk

designing architectures that absorb attacks

chaos security engineering

This is where the better MSc programmes are moving.

3. AI-Era Security (LLM attacks, data poisoning, autonomous agent risk)

This is the biggest gap in traditional programmes.

Core topics:

LLM jailbreaks, alignment drift

model extraction

prompt injection & supply-chain contamination via embeddings

data lineage & trust boundaries

autonomous agent threat models

You are already building complex RAG and agent systems — this pillar will matter a lot.

4. Defensive Engineering & Detection Science

But not SOC Level 1 stuff; rather:

building high-fidelity detections

telemetry design (Otel, eBPF, tracing-driven security)

detection-as-code

reasoning about adversary paths

how defenders get signal through noise

5. Policy, Trust, & Strategic Security (without the GRC fluff)

This is modern:

safety architectures

nation-state capability analysis

platform governance

trust and verification

secure-by-default design decisions

You already think at this level (digital sovereignty, regulatory constraints).
