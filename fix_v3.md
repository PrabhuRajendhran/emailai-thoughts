# Archer — Issues & Fixes by Layer (Time-phased)

---

## 1. Email Layer

**Nature:** low signal, high noise, high volume (~200k/day)

### Core issues

* Raw email text contains signatures, threads, disclaimers
* Same email text reused across stages without a stable canonical form
* PII mixed with semantic content
* Signal is not explicitly surfaced (subject vs body)
* Chunking happens implicitly and inconsistently

---

### Immediate (0–30 days)

* **Centralized ingestion** (already done)
* **Fetch once, store once** (already done)
* **Deterministic canonicalization (non-LLM)**

  * strip signatures, footers, quoted threads
* **PII redaction at ingestion**

  * regex + dictionaries
  * no Comprehend, no LLM
* **Stable canonical email object**

  * single source of truth for all services

**Outcome:** clean, reusable, privacy-safe text with predictable structure

---

### Near term (1–3 months)

* **Signal-first chunking**

  * subject
  * first intent paragraph
  * supporting context (optional)
* **Chunk confidence signals**

  * which chunk supports which label

---

### Longer term (3–6 months)

* Learned signal weights (still outside LLM)
* Continuous rule refinement

---

## 2. Prompt Layer

**Nature:** taxonomy-heavy, instruction-sensitive, fragile

### Core issues

* Taxonomy logic embedded in prompts
* Hierarchy implicitly reasoned by the LLM
* Prompts change when taxonomy changes
* Instruction overhead increases variance and cost

---

### Immediate (0–30 days)

* **Externalize taxonomy logic**

  * hierarchy, exclusions, precedence live in Mongo + code
* **Dynamic taxonomy subset fetch**

  * only labels under predicted parent are retrieved
* **Prompt becomes a pure scoring task**

  * “select best label(s) from this candidate set”

**LLM never reasons about hierarchy.**

---

### Near term (1–3 months)

* **Prompt templating**

  * fixed structure, minimal instructions
* **DSPy (yes, appropriate here)**

  * refine wording, ordering, examples
  * optimize prompt *within a fixed contract*
  * DSPy does *not* encode business rules

---

### Longer term (3–6 months)

* Prompt variants per label family
* Continuous evaluation feedback into DSPy

---

## 3. Model Layer

**Nature:** AWS Bedrock, throttling, cost-sensitive, latency-critical

### Core issues

* Hierarchical fields handled via **sequential LLM calls**
* 5 fields × ~3s = latency explosion
* 100% traffic sent to LLM
* No awareness of model health during routing

---

### Immediate (0–30 days)

* **Collapse hierarchical LLM calls**

  * hierarchy resolved deterministically *before* model invocation
  * **single LLM call** scores all fields together
* **Confidence-gated invocation**

  * embeddings + metadata decide first
  * LLM called only when confidence is low
* **Parallel preparation**

  * embeddings, metadata, taxonomy fetch run concurrently

**Outcome:** LLM is no longer on the critical path by default.

---

### Near term (1–3 months)

* **Rate-aware routing**

  * Bedrock health measured via:

    * throttle ratio (RPM limits)
    * p95 / p99 latency
    * error rates
* **Fallback paths**

  * heuristic / embedding-only classification
* **Speculative execution**

  * prompt & taxonomy prepared while embeddings run

---

### Longer term (3–6 months)

* Multi-model routing
* Cost-aware dynamic thresholds
* Offline LLM audits (not inline dependency)

---

## 4. System Architecture Layer

**Nature:** on-prem microservices, Kafka-driven, Mongo storage

### Core issues

* Sequential execution *inside* the Model Service
* Hierarchy encoded as workflow instead of data
* Latency grows linearly with field depth
* No graceful degradation under model stress

---

### Immediate (0–30 days)

* **Collapse sequential logic inside Model Service**

  * remove per-field LLM calls
* **Kafka events carry IDs only**

  * Mongo remains the source of truth
* **Clear responsibility boundaries**

  * email service: ingestion
  * pre-mapper: deterministic rules
  * model service: scoring only
  * post-mapper: enforcement

---

### Near term (1–3 months)

* **Asynchronous boundaries**

  * fast parent classification (sync)
  * deep classification / enrichment (async)
* **Backpressure propagation**

  * slow Bedrock → reduced upstream rate
* **Graceful degradation**

  * defer non-urgent classifications
  * use fallback classifiers

---

### Longer term (3–6 months)

* SLA-aware routing policies
* Event replay & reprocessing
* Architecture resilient to model outages

---

## Cross-cutting principles (Archer’s spine)

* Hierarchy is data, not reasoning
* Determinism before probability
* Confidence decides *whether* LLM runs
* LLMs score; systems decide
* Degrade gracefully, never catastrophically

---

## One-paragraph executive summary

> Archer’s main issue was treating hierarchical classification as a sequential LLM workflow. The fix is to externalize hierarchy into deterministic logic, collapse multi-field LLM calls into a single scoring pass, and gate model usage using confidence and system health. This converts Archer from an LLM-first pipeline into a resilient, scalable enterprise AI system.

If you want next, I can:

* convert this into a **review-ready slide**
* map it to your **exact service interfaces**
* or show how to **quantify the latency & cost gains**
