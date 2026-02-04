# Archer — Issues & Fixes by Layer (Time-phased)

---

## 1️⃣ Email Layer

### Issues

* Low signal, high noise (threads, signatures, disclaimers)
* Same email fetched & parsed multiple times
* Weak signal buried early, noise dominates models

---

### Fixes

#### Immediate (0–30 days)

* Deterministic canonicalization (non-LLM)
* Strip signatures, quoted threads
* Extract subject + first intent paragraph

**Impact:** lower token cost, better embedding quality

---

#### Near Term (30–60 days)

* Signal-first chunking
* Chunk prioritization (subject → intent → body)
* Persist canonical text + chunks

**Impact:** improved retrieval & confidence gating

---

#### Longer Term (60–90 days)

* Feature materialization as ingestion contract
* Immutable email artifacts (text, chunks, metadata)

**Impact:** no recompute, deterministic reprocessing

---

## 2️⃣ Prompt Layer

### Issues

* Prompt contains taxonomy logic
* Large instruction overhead
* Prompt changes every time taxonomy changes
* High variance & cost

---

### Fixes

#### Immediate (0–30 days)

* Shrink prompt scope
* Candidate-only prompting (Top-K labels)
* Remove hierarchy explanation from prompts

**Impact:** faster, cheaper, more stable LLM behavior

---

#### Near Term (30–60 days)

* Externalize taxonomy logic
* Move hierarchy, exclusions, precedence outside LLM
* Prompt becomes pure scoring interface

**Impact:** taxonomy churn no longer breaks prompts

---

#### Longer Term (60–90 days)

* **Optional: DSPy for prompt refinement**

  * Use DSPy to optimize:

    * label descriptions
    * phrasing consistency
    * scoring instructions
  * DSPy operates on **fixed prompt skeletons**

**Important DSPy note**

> DSPy refines prompts — it does **not** replace routing, confidence gating, or taxonomy logic.

Use DSPy **only after** prompt scope is minimized.

---

## 3️⃣ Model Layer

### Issues

* 100% traffic goes to LLM
* Bedrock TPM / RPM throttling
* High cost & centralized dependency
* No graceful degradation

---

### Fixes

#### Immediate (0–30 days)

* Confidence-based LLM skipping
* Embedding gap + chunk agreement gating

**Impact:** instant cost & latency reduction

---

#### Near Term (30–60 days)

* Tiered model routing

  * heuristics / embeddings
  * cheap model
  * Bedrock LLM (last resort)

**Impact:** LLM handles only ambiguous cases

---

#### Longer Term (60–90 days)

* Rate-aware routing
* Bedrock health as input (GREEN/YELLOW/RED)
* SLA-aware degradation policies

**Impact:** system survives bursts & throttling

---

## 4️⃣ System Architecture Layer

### Issues

* Stateless services re-fetch email from Mongo
* Kafka fan-out causes compute duplication
* No shared feature store
* Latency & infra amplification

---

### Fixes

#### Immediate (0–30 days)

* Centralize email ingestion
* Fetch & clean email once
* Kafka events carry IDs, not payloads

**Impact:** reduced I/O and compute waste

---

#### Near Term (30–60 days)

* Shared feature store
* Canonical text, chunks, embeddings reused
* Stateless workers consume features, not raw data

**Impact:** consistent behavior across services

---

#### Longer Term (60–90 days)

* Model control plane
* Central health, routing, confidence logic
* Unified observability across pipelines

**Impact:** predictable, operable system at scale

---

## Final mental model (very reusable)

> **Clean early, decide cheaply, think only when needed.
> Prompts score; systems decide; LLMs resolve ambiguity.**
