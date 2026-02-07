Here is the **rewritten, structured Email Layer plan** — clean and ready to copy-paste.

---

# Email Layer Architecture

**Nature:** Low signal, high noise, high volume (~200K/day)
**Goal:** Deterministic, stable, privacy-safe canonical email object for all downstream ML services

---

# Core Problems to Solve

* Raw emails contain signatures, disclaimers, and quoted threads
* PII is mixed with semantic signal
* Subject and intent are not explicitly separated
* Cleaning happens inconsistently across services
* No stable canonical form for training & inference
* Thread history dilutes current intent

---

# Design Principle

> All downstream systems consume a single, deterministic Canonical Email Object.
> Raw email is never reused directly.

No LLM in ingestion.
No probabilistic cleaning.
No duplicated preprocessing logic.

---

# Phase 1 — Immediate (0–30 Days)

## 1️⃣ Centralized Ingestion (Single Entry Point)

* Fetch once
* Store once
* All services read from canonical store
* No service re-fetches or re-cleans raw email

---

## 2️⃣ Deterministic Canonicalization (Non-LLM)

### A. Noise Removal (Strictly Rule-Based)

* Strip signatures
* Remove footers and disclaimers
* Remove quoted thread history
* Keep latest customer-authored block
* Optional: retain last agent reply if required for context

### B. PII Redaction at Ingestion

* Regex + dictionaries
* No Comprehend
* No LLM
* Replace PII with consistent tokens (e.g., `<PHONE>`, `<EMAIL>`)

---

## 3️⃣ Stable Canonical Email Object (Explicit Schema)

Example structure:

```
CanonicalEmail {
  email_id
  cleaned_subject
  cleaned_body
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

Rules:

* Deterministic
* Versioned
* Backward compatible
* Single source of truth

---

# Phase 2 — Near Term (1–3 Months)

## 4️⃣ Signal-First Structuring (Still Deterministic)

Instead of arbitrary chunking, define fixed semantic zones:

1. Subject (very high signal)
2. First intent paragraph (highest signal)
3. Remaining body (supporting context)
4. Attachment indicators (if present)

This improves:

* Embedding quality
* Hard negative mining
* Retrieval clarity
* Sibling separation in dense taxonomy regions

---

## 5️⃣ Thread-Aware Truncation Logic

* Remove older conversation depth beyond configurable threshold
* Prefer most recent user-authored content
* Prevent semantic dilution from long threads

---

## 6️⃣ Ingestion Drift Monitoring

Track:

* Average token length
* % content removed as signature
* % emails with empty intent paragraph
* Reply depth distribution
* PII redaction frequency

Purpose:

Detect ingestion drift before it degrades Recall@K.

---

# Phase 3 — Longer Term (3–6 Months)

## 7️⃣ Learned Signal Weighting (Outside LLM)

Still no LLM at ingestion.

Introduce:

* Statistical analysis of which zones drive classification accuracy
* Weighted embedding contributions (subject > first paragraph > body)
* Continuous rule refinement based on error analysis

---

# What This Enables Downstream

* Cleaner embedding geometry
* Better hierarchy-aware negative separation
* Stable silver data mining
* More reliable cross-encoder reranking
* Lower noise in distillation
* Predictable Recall@K performance

---

# Strict Non-Negotiables

* No LLM in ingestion
* No duplicated cleaning across services
* No raw email reuse downstream
* Deterministic transformations only
* Canonical schema versioning

---

# Final Outcome

A clean, reusable, privacy-safe, structured Canonical Email Object that:

* Scales to 200K/day
* Improves retrieval stability
* Reduces sibling confusion
* Enables continuous learning
* Protects downstream model geometry from ingestion noise

---

If you want, I can now align this explicitly with the retrieval + hierarchy-weighted MNR pipeline in one unified end-to-end architecture document.
