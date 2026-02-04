# Archer — Issues & Fixes by Layer (Time-phased)

## 1. Email Layer

**Nature:** low signal, high noise, high volume (200k/day)

### Core issues

* Same email fetched repeatedly by downstream services
* No deterministic canonical form
* PII mixed with semantic text
* Signal diluted by signatures, threads, disclaimers
* Chunking happens late and inconsistently

---

### Immediate (0–30 days)

* **Centralized ingestion** (already done)
* **Fetch once, store once** (already done)
* **Kafka events carry IDs only** (already done)
* **Deterministic canonicalization (non-LLM)**

  * strip signatures, footers, quoted threads
* **PII redaction at ingestion**

  * regex + dictionaries (no Comprehend, no LLM)

Result: stable, reusable, privacy-safe email text

---

### Near term (1–3 months)

* **Signal-first chunking**

  * subject
  * first intent paragraph
  * supporting context (optional)
* **Chunk confidence signals**

  * which chunk voted for which label

---

### Longer term (3–6 months)

* Learned signal weights (still outside LLM)
* Continuous regex + dictionary refinement

---

## 2. Prompt Layer

**Nature:** messy taxonomy, instruction overload, fragile prompts

### Core issues

* Taxonomy logic embedded in prompts
* Long prompts = cost + variance
* No separation between *reasoning* and *rules*
* Prompt changes required when taxonomy changes

---

### Immediate (0–30 days)

* **Externalize taxonomy logic**

  * hierarchy, exclusions, precedence live in Mongo + code
* **Fetch only taxonomy subset**

  * based on predicted parent category
* **Prompt = scoring task only**

  * “Pick best label from this candidate set”

---

### Near term (1–3 months)

* **Prompt templating**

  * stable structure
  * minimal instructions
* **DSPy usage (yes, appropriate here)**

  * refine *wording*, ordering, examples
  * optimize for accuracy *within fixed structure*
  * DSPy does **not** own business logic

---

### Longer term (3–6 months)

* Prompt variants per label family
* Auto-evaluation loops feeding DSPy

---

## 3. Model Layer

**Nature:** AWS Bedrock, throttling, high cost, variable latency

### Core issues

* 100% traffic routed to LLM
* Sequential calls → latency explosion
* RPM / TPM throttling
* No notion of model health in routing

---

### Immediate (0–30 days)

* **Confidence-gated LLM invocation**

  * embeddings + metadata decide first
  * LLM only when confidence is low
* **Parallel fan-out**

  * embeddings, metadata scoring, health checks run concurrently
* **Skip LLM entirely for high-confidence cases**

---

### Near term (1–3 months)

* **Rate-aware routing**

  * Bedrock health as an input:

    * throttle ratio (quota-based)
    * p95 / p99 latency
    * error rates
* **Fallbacks**

  * heuristic / embedding-only classifier
* **Speculative execution**

  * prepare prompts & taxonomy while embeddings run

---

### Longer term (3–6 months)

* Multi-model routing
* Cost-aware dynamic thresholds
* Offline LLM audits instead of inline calls

---

## 4. System Architecture Layer

**Nature:** on-prem microservices, Kafka-driven, Mongo storage

### Core issues

* Sequential microservice calls
* Repeated DB fetches
* Tight coupling between stages
* No graceful degradation under load

---

### Immediate (0–30 days)

* **Fan-out / fan-in pattern**

  * parallel consumers, not chained calls
* **Single consumer per responsibility**

  * not “one consumer total”
* **No payload hopping**

  * IDs only, shared storage

---

### Near term (1–3 months)

* **Asynchronous boundaries**

  * fast parent classification
  * async deep classification
* **Backpressure propagation**

  * slow model → upstream throttling
* **Graceful degradation**

  * defer non-urgent classifications

---

### Longer term (3–6 months)

* SLA-aware routing policies
* Event replay + reprocessing
* Architecture resilient to model outages

---

## Cross-cutting principles (the Archer philosophy)

* Determinism before probability
* Confidence decides *whether* LLM is called
* LLMs score; systems decide
* Taxonomy is data, not prompt text
* Degrade gracefully, never catastrophically

---

## One-paragraph executive summary

> Archer’s core problem is not model quality but sequential, LLM-centric design. The fix is deterministic preprocessing, confidence-gated model invocation, externalized taxonomy logic, and parallel, rate-aware system architecture. LLMs become an escalation path, not the default.

