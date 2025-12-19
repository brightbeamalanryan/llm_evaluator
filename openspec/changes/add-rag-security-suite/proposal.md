# Context

## Purpose

Build an internal **LLM/RAG Security Evaluation Framework** with a dedicated **adversarial RAG target** used for red-team testing.

The goal is to systematically identify, reproduce, and regress-test:

* prompt and policy leakage,
* instruction hierarchy failures,
* RAG-specific attack vectors,
* metadata and template exposure,
* hallucinated or invented policy exceptions,
* guard model blind spots.

This project exists to close the **largest blind spot in production RAG deployments**: security failures introduced by retrieval pipelines.

---

## Why

RAG (Retrieval-Augmented Generation) systems introduce **unique and under-tested attack surfaces** through the retrieval pipeline.

Malicious or malformed retrieved content can:

* override system instructions,
* poison downstream reasoning,
* induce hallucinated internal rules,
* leak metadata or prompt scaffolding,
* bypass safety or privacy constraints.

Most existing eval frameworks focus on **answer correctness**, not **prompt integrity or policy invariants under adversarial retrieval**. This project explicitly targets that gap.

---

## Tech Stack

* **Python 3.x**
* **Ollama** (local inference + `/api/chat`)
* **Local LLMs**

  * Target models: `llama3.1:8b`, `qwen2.5:7b-instruct`, etc.
  * Guard models: `phi`, `llama3.1:8b`
  * Mutator model: `prompt-mutator` (custom Ollama Modelfile, Dolphin-based) create a Modelfile dir to store, these. An example is available in ./local_models/Modelfile
* **In-memory retrieval**

  * v1: BM25 / TF-IDF
  * v2 (optional): embeddings + cosine similarity
* **rich** (CLI output)
* **jq / curl** (debugging)
* Optional extras:

  * ChromaDB / Pinecone (vector store realism)
  * pytest
  * Pydantic / JSONSchema
  * CI (GitHub Actions / GitLab CI)

---

## Project Conventions

### Code Style

* Security evals over abstraction cleverness.
* Explicit, readable Python.
* Prompts treated as **versioned data**, not inline strings.
* Everything logged that is needed to reproduce a failure:

  * model + tag
  * sampling params
  * policy surface
  * retrieved context
  * final prompt (debug mode only)
  * model reply
  * guard decision + rationale

### Architecture Patterns

* **Eval Harness** executes structured test cases.
* **Three-role evaluation loop (optional)**:

  1. **Target** → generates response
  2. **Guard** → evaluates compliance / leakage
  3. **Mutator** → proposes next adversarial probes
* **Policy Surface Abstraction**:

  * Never rely on literal system prompt text.
  * Evaluate against *declared* or *observed* policy invariants.

### Testing Strategy

* Security evals act as **regression tests**.
* Any change to:

  * RAG prompt template,
  * retrieval logic,
  * system policy,
  * or model version
    must not increase leakage or bypass rates.
* Manual judgement supported initially; guard accuracy tracked (FP/FN).
* Canary tokens and simple heuristics used to augment guard models.

### Git Workflow

* Test cases are first-class artifacts (JSON).
* RAG corpora changes require review.
* Branches:

  * `main`
  * `feat/rag-security-*`
* Commits reference:

  * attack class
  * affected policy surface
  * expected behavioural change

---

## Domain Context

### System Prompt Reality in RAG

In production, the “system prompt” is **not a single string**.
It is a **runtime-assembled context** including:

* safety and privacy policy,
* domain role instructions,
* output formatting rules,
* tool usage constraints,
* retrieval scaffolding,
* hidden metadata and glue logic.

### Policy Surface (Core Abstraction)

For evaluation purposes, the system prompt is represented as a **policy surface**, derived in one of three ways:

1. **Declared policy surface**
   Human-authored description of required invariants.

2. **Observed policy surface**
   Inferred from refusal language or behaviour.

3. **Composite system context (advanced)**
   Structured description of domain, constraints, tools, and RAG settings.

Security testing focuses on **whether invariants hold**, not on extracting literal prompt text.

---

## Adversarial RAG Target

### Description

A **simple, local RAG target** designed specifically to be attacked.

Characteristics:

* Documents loaded from a local directory (`./docs_source`)
* Entirely **in memory**
* Minimal retrieval logic
* Transparent prompt template (versioned)
* Optional debug mode exposing assembled prompts for internal testing

This target is intentionally minimal to make failures attributable and reproducible.

### Pipeline

1. Load documents from `./docs_source`
2. Chunk documents (fixed window + overlap)
3. Build in-memory index (BM25 / TF-IDF)
4. For each query:

   * retrieve top-k chunks
   * assemble system policy + retrieved context
   * call target LLM via Ollama
   * return answer + citations

---

## What Changes

This project introduces explicit **RAG-focused security testing**, including:

* Context injection attack tests (JSON-based)
* Retrieval override attempt detection
* Prompt template inversion tests
* Metadata leakage detection
* Multi-hop RAG attack simulation
* Optional vector store integration for realistic testing

These tests extend existing prompt-security evals into the retrieval layer.

---

## Reused Components

* `HallucinatedRuleDetector`
  (`src/eval_fw/guard/meta_evaluator.py`)

This detector is reused to identify:

* invented policy exceptions,
* hallucinated “rules”,
* fabricated permission lists derived from retrieved content.

---

## Implementation Notes

* Test cases live in:

  * `use_cases/rag_tests.json`
  * consistent with existing `bypass_tests.json` format
* New module location:

  * `src/eval_fw/rag/`
* Vector store integrations (ChromaDB, Pinecone):

  * optional extras, not hard dependencies
* Debug mode:

  * allows prompt capture for internal analysis
  * disabled in normal runs

---

## Important Constraints

* Local-only by default (no external services required).
* Synthetic data only for secrets / PII.
* Deterministic retrieval for reproducible evals.
* No reliance on hidden or proprietary system prompt text.
* Focus on **policy invariant enforcement**, not jailbreak theatrics.

---

## External Dependencies

* **Ollama** runtime and HTTP API
* Optional:

  * Vector DBs (ChromaDB, Pinecone)
  * CI runner environment
  * Log aggregation / artefact storage

