Here is the **Unified End-to-End Production Architecture Blueprint** — complete, structured, and ready to copy-paste.

---

# Unified Email Classification Architecture

**Scale:** ~200K emails/day
**Constraint:** Single-label mandatory
**Taxonomy:** Hierarchical, overlapping
**Objective:** High precision, scalable, continuously improving system

---

# 1️⃣ System Overview

Raw Email
↓
**Email Layer (Canonicalization)**
↓
**Pre-Router (Deterministic Gate)**
↓
**ML Pipeline (Retrieval → Conditional Rerank)**
↓
**Post-Router (Governance Gate)**
↓
Final Label
↓
Logging & Continuous Learning Loop

---

# 2️⃣ Email Layer — Canonicalization Foundation

## Nature

Low signal, high noise, high volume.

## Goals

* Deterministic preprocessing
* Privacy-safe data handling
* Stable canonical email object
* Single source of truth

---

## 2.1 Deterministic Cleaning (Non-LLM)

* Strip signatures, footers, disclaimers
* Remove quoted threads
* Keep latest customer-authored block
* Optional: retain last agent reply (configurable)
* PII redaction using regex + dictionaries
* Replace PII with stable tokens (e.g., `<PHONE>`, `<EMAIL>`)

No LLM.
No probabilistic cleaning.

---

## 2.2 Canonical Email Object (Versioned Schema)

Example:

```
CanonicalEmail {
  email_id
  cleaned_subject
  latest_customer_block
  first_intent_paragraph
  structured_chunks[]
  pii_redacted_text
  metadata {
     language
     reply_depth
     has_attachment
     ingestion_timestamp
  }
}
```

All downstream services consume only this object.

---

## 2.3 Ingestion Monitoring

Track:

* Avg token length
* % signature stripped
* % empty intent paragraphs
* Reply depth distribution
* PII redaction frequency

Purpose: Prevent silent degradation of retrieval quality.

---

# 3️⃣ Pre-Router — Deterministic Gate

## Purpose

Reduce ML load and resolve obvious cases.

## Allowed Rule Categories

* Exact structural patterns (ticket IDs, order IDs)
* Known system templates
* Source-system routing headers
* Exact, unique phrases tied to one label

Rules must be:

* High precision
* Deterministic
* Version-controlled
* Auditable

If ambiguity exists → route to ML.

Target: 10–20% resolution via Pre-Router.

---

# 4️⃣ ML Pipeline — Core Semantic Engine

---

# 4.1 Bi-Encoder (Retrieval Layer)

## Role

Fast semantic retrieval.

## Flow

Canonical Email
→ Encode email
→ Compare with label embeddings
→ Retrieve Top-20 candidates

## Training

* Domain-adaptive pretraining (MLM)
* Multiple Negatives Ranking (MNR)
* Hierarchy-weighted negative scaling
* Hard negative mining (siblings + confusions)

## Target Metric

Recall@5 ≥ 97–98%

---

# 4.2 Conditional Margin Routing

If:

(top1_score − top2_score) ≥ calibrated threshold
AND
top1_score ≥ confidence floor

→ Assign label directly

Else → Send to Cross-Encoder

---

# 4.3 Cross-Encoder (Precision Layer)

## Role

Resolve sibling overlap and subtle distinctions.

## Flow

(email + Top-K candidates)
→ Joint encoding
→ Listwise softmax competition
→ Select Top-1

## Training

* Listwise Softmax + Cross-Entropy
* Inject sibling confusions
* Inject hard negatives
* Train on user corrections (gold data)

---

# 5️⃣ Post-Router — Governance Gate

## Purpose

Validate and enforce business constraints.

## Responsibilities

* Enforce single-label requirement
* Validate label eligibility
* Enforce regulatory routing priorities
* Reject low-confidence predictions
* Route ambiguous cases to manual review

Override rate should remain <5%.

---

# 6️⃣ Logging & Data Engine

For every email, log:

* Top-K candidates
* Similarity scores
* Cross-encoder scores
* Score margins
* Final label
* User corrections
* Routing path (rule / retrieval / rerank)

This fuels continuous learning.

---

# 7️⃣ Continuous Learning Loop

Runs weekly or biweekly.

---

## 7.1 Silver Data Mining

High-confidence predictions:

* Large margin
* High calibrated confidence

Generate:

(email, predicted_label)
Hard negatives = sibling + near neighbors

---

## 7.2 Gold Data Collection

From user corrections:

(email, correct_label)
(email, wrong_label)

High-value hard negatives.

---

## 7.3 Cross-Encoder Fine-Tuning

Train using:

Listwise Softmax + CE
Focus on tight sibling clusters.

---

## 7.4 Distillation (Cross → Bi)

* Cross-encoder generates soft ranking distributions
* Train bi-encoder using:

  * MNR (primary)
  * KL divergence (optional)

Improves retrieval geometry.

---

## 7.5 Evaluation Metrics

Track:

* Recall@K
* Top-1 accuracy
* Sibling confusion rate
* Margin distribution
* Cross-encoder usage rate
* Drift metrics

---

# 8️⃣ Hierarchical Overlap Strategy

Handled via:

* Hierarchy-weighted MNR
* Sibling hard negative mining
* Listwise reranking competition
* Confusion-driven sampling
* Distillation feedback

No explicit tree-softmax required.

---

# 9️⃣ Target Operational Distribution

At scale:

* 10–20% Pre-Router
* 60–70% High-margin retrieval
* 10–20% Cross-Encoder rerank

Ensures cost control + precision.

---

# 10️⃣ Core Design Principles

1. Deterministic ingestion foundation
2. Retrieval optimized for geometry (Recall@K)
3. Reranking optimized for competition (Listwise)
4. Rules for certainty, ML for ambiguity
5. Governance after prediction
6. Continuous feedback refinement
7. Hierarchical structure injected via loss weighting

---

# Final End-to-End Flow

Raw Email
→ Canonical Email Layer
→ Pre-Router
→ Bi-Encoder Retrieval
→ Conditional Margin Gate
→ Cross-Encoder (if needed)
→ Post-Router
→ Final Label
→ Logging
→ Continuous Learning

---

This architecture is:

* Scalable to 200K/day
* Robust to hierarchical overlap
* Privacy-safe
* Cost-efficient
* Continuously improving
* SLA-stable
* Taxonomy-evolution ready

---

If you’d like, I can next produce a **phased 6-month execution roadmap** mapped to engineering milestones and measurable KPIs.
