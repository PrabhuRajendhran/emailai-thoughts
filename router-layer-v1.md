Here is the **Pre-Router + Post-Router Architecture Plan** — clean, structured, and ready to copy-paste.

---

# Router Layer Architecture

**Position:** Surrounds the ML pipeline
**Purpose:** Control cost, enforce governance, preserve accuracy
**Scale:** ~200K emails/day

---

# Overall Flow

Canonical Email
↓
**Pre-Router (Deterministic Gate)**
↓
ML Pipeline (Bi-Encoder → Conditional Cross-Encoder)
↓
**Post-Router (Governance Gate)**
↓
Final Label

---

# 1️⃣ Pre-Router — Deterministic Gate

## Purpose

* Reduce unnecessary ML load
* Resolve obvious cases deterministically
* Enforce structural routing rules
* Protect latency and compute cost

Pre-Router decides:

> “Do we even need ML for this email?”

---

## What Pre-Router Is Allowed To Do

### A. Structural Pattern Routing

* Exact ticket/order ID formats
* Known system-generated templates
* Machine-originated emails
* Regulatory-required fixed mappings

### B. Metadata-Based Routing

* Known sender domains
* Internal automation emails
* Source-system routing headers
* Explicit routing fields

### C. Strict Phrase Matching (Exact Only)

* Hard-coded phrases uniquely tied to a label
* No fuzzy matching
* No semantic inference

---

## Confidence Requirement

Rules must be:

* Near-zero false positive
* Deterministic
* Version-controlled
* Auditable

If ambiguity exists → send to ML pipeline.

No probabilistic rules.

---

## Guardrails

Pre-Router must NOT:

* Perform semantic classification
* Compete with ML in overlapping taxonomy areas
* Use heuristic confidence scoring
* Expand into rule-heavy classification engine

---

## Monitoring

Track:

* % emails resolved by Pre-Router
* Precision of rule-triggered assignments
* Drift in rule trigger rates

Target range:

10–20% deterministic resolution at scale.

---

# 2️⃣ Post-Router — Governance Gate

## Purpose

* Validate ML output
* Enforce business constraints
* Ensure compliance
* Apply policy overrides when required

Post-Router decides:

> “Is this ML prediction acceptable under business rules?”

---

## What Post-Router Is Allowed To Do

### A. Policy Enforcement

* Enforce single-label requirement
* Validate label eligibility for sender type
* Enforce regulatory routing priorities

### B. Confidence Safeguards

* If similarity margin below calibrated threshold → flag
* If cross-encoder confidence low → fallback queue
* If top predictions extremely close → manual review

### C. Conflict Resolution

* If metadata contradicts label
* If attachment type incompatible with predicted category
* If restricted label predicted without required fields

---

## Fallback Options

If Post-Router rejects prediction:

* Route to manual review
* Route to fallback default label (if business-approved)
* Trigger secondary validation workflow

---

## Guardrails

Post-Router must NOT:

* Re-classify semantically
* Override model decisions based on weak heuristics
* Introduce subjective logic
* Drift into alternate classifier

---

## Monitoring

Track:

* % predictions overridden
* Override reasons distribution
* Confidence rejection rate
* Manual review volume

Override rate should remain low (<5%).

---

# Final Combined Decision Logic

1. Canonical Email created
2. Apply Pre-Router

   * If deterministic rule matches → Assign label
3. Else → Bi-Encoder retrieval

   * If high margin → Assign label
   * Else → Cross-Encoder rerank
4. Apply Post-Router

   * If valid → Final label
   * If invalid → Fallback / Review

---

# Outcome

This dual-router architecture:

* Reduces ML cost
* Preserves precision
* Enforces governance
* Prevents rule explosion
* Supports evolving taxonomy
* Scales to high volume

---

If needed, I can now produce the full end-to-end system blueprint (Email Layer + Routers + Retrieval + Rerank + Continuous Learning) as a single unified production architecture document.
