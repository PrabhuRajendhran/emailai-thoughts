Here is the **final recommended production pipeline**, clean and ready to copy-paste.

---

# FINAL RECOMMENDED PIPELINE

*(200K emails/day | Single-label mandatory | Hierarchical, overlapping taxonomy | Limited initial gold data)*

---

## STAGE 0 — Base Models

* Strong pretrained **sentence embedding model** (E5 / BGE / SBERT / MPNet-based)
* Strong pretrained **cross-encoder** (MSMARCO/NLI fine-tuned)

Do NOT start from raw BERT.

---

## STAGE 1 — Domain Adaptation (Before Heavy Training)

Perform lightweight **Domain Adaptive Pretraining (MLM)** on:

* Historical emails
* Label descriptions
* Internal documents

Goal:

* Reduce domain vocabulary mismatch
* Improve contextual understanding before contrastive training

---

## STAGE 2 — Initial Inference (Cold Start Deployment)

### Inference Flow

Email
↓
Bi-Encoder → Retrieve Top-20
↓
Cross-Encoder → Rerank Top-5
↓
Select Top-1

Store for each request:

* Top-K candidates
* Cross-encoder scores
* Score margins
* User corrections (if any)

---

## STAGE 3 — Silver Data Bootstrapping

From production traffic:

Select high-confidence predictions using:

* Large score(top1) − score(top2)
* Top1 score above calibrated threshold

Create silver dataset:

Positive:

* (email, predicted_label)

Negatives:

* Other top-K candidates
* Sibling labels (important)
* Near embedding neighbors

---

## STAGE 4 — Train Bi-Encoder (Core Retrieval Model)

Train using:

**Multiple Negatives Ranking (MNR) Loss**

Training data:

* Silver positives
* In-batch negatives
* Explicit hard negatives (siblings + model confusions)

Target metric:

* Recall@5 ≥ 97%

Goal:
Ensure correct label is almost always inside Top-K.

---

## STAGE 5 — Feedback Collection (Gold Data Emerges)

From user corrections:

Collect:

* (email, correct_label)
* (email, wrong_label)

This becomes high-quality gold data with strong hard negatives.

---

## STAGE 6 — Fine-Tune Cross-Encoder (Accuracy Layer)

Train using:

**Listwise Softmax + Cross-Entropy**

Training format:
(email + Top-K candidate set)

Why listwise:
Inference = choose 1 winner among K candidates.

Inject:

* User corrections
* Hard sibling confusions
* Close semantic competitors

Goal:
Maximize top-1 precision.

---

## STAGE 7 — Distillation (Cross → Bi)

After cross-encoder improves measurably:

1. Score candidate sets using cross-encoder.
2. Generate soft ranking distributions.
3. Train bi-encoder to mimic ranking behavior.

Loss:

* MNR (primary)
* KL divergence to teacher distribution (optional but recommended)

Goal:
Transfer fine-grained discrimination into retrieval model.
Reduce cross-encoder burden over time.

---

## STAGE 8 — Continuous Learning Cycle (Weekly/Biweekly)

1. Aggregate new feedback.
2. Fine-tune cross-encoder (listwise).
3. Distill into bi-encoder.
4. Re-evaluate:

   * Recall@K
   * Top-1 accuracy
   * Sibling confusion rate
   * Drift metrics

---

# STABLE INFERENCE FLOW (Final Production)

Email
↓
Bi-Encoder (fast retrieval)
↓ Top-20
Cross-Encoder (accurate rerank)
↓ Top-1
Return Label

---

# TRAINING OBJECTIVES SUMMARY

Bi-Encoder → Multiple Negatives Ranking (MNR)
Cross-Encoder → Listwise Softmax + Cross-Entropy
Distillation → KL Divergence (optional enhancement)

---

# DESIGN PRINCIPLES

1. Optimize embedding geometry for retrieval (MNR)
2. Optimize joint competition for final decision (Listwise)
3. Use cross-encoder as teacher
4. Inject hard negatives aggressively
5. Align training objective with inference behavior
6. Continuously learn from user feedback

---

This pipeline is:

* Scalable to 200K/day
* Robust to overlapping hierarchical taxonomy
* Minimal initial gold requirement
* Improvement-driven via feedback
* SLA-safe

---

Here’s the **one-page executive summary version** — clean, stakeholder-ready.

---

# Email Classification System — Production Architecture

### Scale

* 200K emails/day
* Single-label mandatory
* Hierarchical & overlapping taxonomy
* Continuous learning required

---

# 1️⃣ High-Level Architecture

### Inference Flow

Email
→ **Bi-Encoder (Fast Retrieval)** → Top-20 Candidates
→ **Cross-Encoder (Accurate Rerank)** → Top-1 Label
→ Return Prediction

This design separates:

* **Speed layer** (retrieval)
* **Accuracy layer** (reranking)

---

# 2️⃣ Core Model Strategy

### Retrieval Model (Bi-Encoder)

* Domain-adapted pretrained embedder
* Trained using **Multiple Negatives Ranking (MNR)**
* Optimized for high Recall@K (≥97%)

Purpose:
Ensure correct label is almost always retrieved.

---

### Accuracy Model (Cross-Encoder)

* Jointly encodes email + candidate label
* Trained using **Listwise Softmax + Cross-Entropy**
* Optimized for top-1 precision

Purpose:
Choose the best label among retrieved candidates.

---

# 3️⃣ Data Strategy (Minimal Gold Start)

### Phase 1 — Cold Start

* Use pretrained models
* Log predictions + score margins

### Phase 2 — Silver Data

* High-confidence predictions become silver positives
* Hard negatives mined from siblings & confusions

### Phase 3 — Gold Data via Feedback

* User corrections produce high-value supervised pairs

---

# 4️⃣ Continuous Learning Loop

Weekly/Biweekly:

1. Add new user feedback
2. Fine-tune Cross-Encoder (accuracy improves)
3. Distill into Bi-Encoder (retrieval improves)
4. Monitor:

   * Recall@K
   * Top-1 Accuracy
   * Confusion among siblings
   * Drift metrics

---

# 5️⃣ Why This Works

* Scales to high volume
* Handles overlapping taxonomy
* Reduces manual labeling cost
* Maintains SLA stability
* Improves continuously
* Supports taxonomy evolution

---

# 6️⃣ Training Objectives

| Layer         | Objective                        |
| ------------- | -------------------------------- |
| Bi-Encoder    | Multiple Negatives Ranking (MNR) |
| Cross-Encoder | Listwise Softmax + CE            |
| Distillation  | KL Divergence (optional)         |

---

# Strategic Design Principles

* Separate retrieval from decision
* Align training with inference
* Aggressive hard-negative mining
* Teacher–student refinement
* Continuous feedback integration

---

Here is a **clear visual architecture diagram description** you can hand to a designer, architect, or convert directly into a slide.

---

# Visual Architecture Diagram — Email Classification System

## 🎯 Diagram Style

Use a **3-layer horizontal flow**:

**Input Layer → Retrieval Layer → Accuracy Layer → Output Layer**

Below that, show a **Feedback & Training Loop** flowing backward.

---

# 🔷 TOP SECTION — ONLINE INFERENCE PIPELINE

### 1️⃣ Input Layer (Left)

Box:

**Incoming Email**

* Raw email text
* Metadata (optional)

Arrow →

---

### 2️⃣ Retrieval Layer (Fast Path)

Large box labeled:

**Bi-Encoder (Embedding Model)**
Subtitle: *Domain-adapted | MNR-trained*

Inside the box:

* Encode Email → Vector
* Compare with Label Vectors
* Retrieve Top-20

Arrow →

Small output box:

**Top-20 Candidate Labels**

---

### 3️⃣ Accuracy Layer (Precision Engine)

Large box labeled:

**Cross-Encoder (Reranker)**
Subtitle: *Listwise-trained*

Inside the box:

* Joint encode (Email + Candidate)
* Score each candidate
* Softmax competition

Arrow →

Small output box:

**Top-1 Label**

Arrow →

---

### 4️⃣ Output Layer

Box:

**Final Predicted Label**

* Returned to system
* Logged for monitoring

---

# 🔷 MIDDLE SECTION — Logging & Monitoring

From both models, arrows down to:

**Prediction Log Store**

Stored:

* Top-K candidates
* Cross-encoder scores
* Score margins
* User corrections
* Timestamps

---

# 🔷 BOTTOM SECTION — CONTINUOUS LEARNING LOOP

This section flows right-to-left (feedback loop).

---

### A. Data Curation Module

Box:

**Data Engine**

Inputs:

* High-confidence predictions → Silver data
* User corrections → Gold data
* Hard negatives (siblings + confusions)

Arrow →

---

### B. Cross-Encoder Training

Box:

**Cross-Encoder Fine-Tuning**

* Listwise Softmax + CE
* Focus: Top-1 precision

Arrow →

---

### C. Distillation Module

Box:

**Knowledge Distillation**

* Cross-encoder = Teacher
* Bi-encoder = Student
* KL + MNR loss

Arrow →

---

### D. Bi-Encoder Training

Box:

**Bi-Encoder Contrastive Training**

* Multiple Negatives Ranking
* Hard negative mining
* Recall@K optimization

Arrow back up to:

Retrieval Layer (closing loop)

---

# 🔷 SIDE PANEL — Evaluation Metrics (Right Side)

Vertical metrics box:

**Online Metrics**

* Recall@5
* Top-1 Accuracy
* Sibling Confusion Rate
* Latency (SLA)
* Drift Monitoring

---

# 🔷 Optional — Hierarchy Awareness Indicator

Add small annotation near retrieval layer:

“Hierarchy-aware hard negative mining”

And near reranker:

“Sibling competition emphasis”

---

# 🎨 How It Should Visually Feel

* Top = Online flow (left → right)
* Bottom = Training loop (right → left)
* Clear separation:

  * Speed layer (bi-encoder)
  * Precision layer (cross-encoder)
* Feedback loop visually prominent

---

# Ultra-Concise Slide Version (If Needed)

Title:
**Scalable Two-Stage Email Classification with Continuous Learning**

Center:
Retrieval → Rerank → Feedback → Retrain → Improve

---

Yes — you’re remembering correctly.

Earlier we discussed **injecting hierarchical structure directly into the loss**, not just handling it via hard negatives.

Let me restate it clearly.

---

# What We Discussed: Hierarchy-Aware Loss Injection

The idea was:

> Don’t treat all negatives equally.
> Penalize errors differently depending on taxonomy distance.

Instead of flat contrastive loss, we make it **hierarchy-aware**.

There were three main approaches.

---

# 1️⃣ Distance-Weighted Contrastive Loss (Bi-Encoder)

In normal MNR:

All negatives are treated equally.

In hierarchy-aware MNR:

You weight negatives based on tree distance.

Example:

If true label = L3
Sibling label = L3b
Different branch label = L9

You assign:

* Higher penalty for confusing L3 vs L3b
* Lower penalty for confusing L3 vs L9

Because sibling confusion is worse.

Formally:

Loss weight ∝ 1 / (tree_distance + ε)

This forces sharper sibling separation.

---

# 2️⃣ Hierarchical Soft Labels (Cross-Encoder)

Instead of one-hot target:

You create a soft distribution.

Example:

True label probability = 1.0
Sibling labels = 0.1
Other labels = 0.01

Then normalize.

This teaches:

“Sibling is wrong, but less wrong than distant label.”

This smooths training and stabilizes tight clusters.

---

# 3️⃣ Parent-Child Multi-Task Loss (Optional)

Predict:

* Parent category
* Child category

Total loss:

L = L_parent + L_child

This enforces structural awareness.

But we deprioritized this because:

You require single-label final output,
not hierarchical multi-output.

---

# Why We Didn’t Make It Core

Because your current pipeline already handles hierarchy via:

* Hard negative mining
* Listwise competition
* Confusion injection

Explicit hierarchy loss adds complexity and tuning overhead.

It’s powerful — but not necessary for v1.

---

# When Hierarchy-Aware Loss Is Actually Worth It

Add it if:

* Sibling confusion remains dominant after training
* Cross-encoder struggles even with listwise setup
* Taxonomy depth ≥ 3 levels
* Many labels per parent (≥10 children)

Then hierarchy-aware weighting can help.

---

# Clean Practical Recommendation

For now:

* Keep sibling hard negatives.
* Keep listwise training.

If confusion persists:

Add **distance-weighted negative scaling in bi-encoder MNR**.

That’s the safest injection point.

---

# What You Were Remembering

We discussed:

> Injecting tree-distance weighting into contrastive loss.

Yes — that’s the correct memory.

---

If you want, I can now:

* Write the exact modified MNR formula with hierarchy weighting
* Or simulate how this changes gradient behavior
* Or explain when hierarchy-aware loss actually harms performance

Which direction?

Perfect — let’s make this **simple and intuitive**.

No heavy math. Just the core idea.

---

# The Problem

In normal MNR training:

All wrong labels are treated equally.

But in your taxonomy:

* Confusing **Billing vs Invoice** (siblings) is a big mistake.
* Confusing **Billing vs Shipping** (different branch) is less likely and less harmful.

Standard MNR does not know this.

So siblings often stay too close in embedding space.

---

# The Simple Fix

We change the loss so that:

> The model pushes sibling labels away **harder** than distant labels.

That’s it.

---

# Normal MNR (Conceptually)

The loss says:

“Make the correct label closer than all others.”

All negatives pull equally.

---

# Hierarchy-Aware MNR (Conceptually)

The loss now says:

“Make the correct label closer,
and push sibling labels away **extra hard**.”

So instead of:

All negatives = same strength

We use:

Sibling negative = strong push
Distant negative = weak push

---

# How We Do It (Very Simple Formula)

For each wrong label:

We multiply its penalty by a weight:

```
weight = 1 / (tree_distance + small_number)
```

So:

| Label Type | Distance | Weight | Effect           |
| ---------- | -------- | ------ | ---------------- |
| Sibling    | 1        | High   | Strong push away |
| Cousin     | 2        | Medium | Medium push      |
| Far label  | 3+       | Low    | Light push       |

That’s the entire modification.

---

# What Happens to Gradients (Intuition)

During training:

Without hierarchy weighting:

* Model spreads everything apart evenly.

With hierarchy weighting:

* Model creates stronger local separation.
* Dense sibling clusters get cleaner boundaries.

It reshapes the embedding space like this:

Before:

```
Billing – Invoice – Payment (too close)
```

After:

```
Billing      Invoice
      \      /
       Email
```

Cleaner structure.

---

# Why This Helps You

Because your real pain is:

Sibling confusion.

This modification directly attacks that.

It improves:

* Retrieval quality in dense branches
* Cross-encoder reranking stability
* Overall top-1 accuracy

---

# Important: It Doesn’t Break Retrieval

We are NOT:

* Changing positives
* Removing negatives
* Changing inference

We are only scaling how strongly certain negatives affect training.

So recall stays stable.

---

# When To Use It

Use this if:

* You see sibling confusion dominating errors
* Embeddings cluster siblings too tightly
* Cross-encoder is working too hard

---

# One-Line Summary

Hierarchy-weighted MNR =
“Push similar wrong labels away harder than distant wrong labels.”

That’s it.

---

Yes — and more importantly, it fits **cleanly and safely** into your email-layer pipeline without changing the architecture.

Let’s connect it directly to your existing system so it’s crystal clear.

---

# Where It Fits in Your Pipeline

Your current production design:

Email
→ **Bi-Encoder (Retrieval)**
→ Top-20
→ **Cross-Encoder (Rerank)**
→ Top-1

Hierarchy-weighted MNR modifies only:

> 🔷 Stage 4 — Bi-Encoder Training

It does NOT change:

* Inference flow
* Cross-encoder
* Distillation
* Latency
* Storage
* Logging

So yes — it aligns perfectly.

---

# Why It’s Especially Aligned With Your Email Layer

Remember your constraints:

* Hierarchical overlapping taxonomy
* Single-label mandatory
* Sibling confusion is dominant
* 200K emails/day (so retrieval must be strong)

Hierarchy-weighted MNR strengthens exactly what retrieval needs:

> Clean separation inside dense sibling clusters.

That improves:

* Recall@K in tight branches
* Candidate quality for cross-encoder
* Stability under taxonomy growth

---

# How It Interacts With the Cross-Encoder

Very nicely.

Bi-Encoder (with hierarchy weighting):

* Creates better local geometry
* Reduces extreme sibling overlap

Cross-Encoder:

* Still resolves final subtle differences
* Works with cleaner candidate sets

So:

Retrieval becomes smarter
Reranker becomes sharper

They don’t conflict.

---

# Does It Break Silver Data or Distillation?

No.

In fact:

* Silver mining becomes cleaner (fewer ambiguous near-ties)
* Distillation becomes more stable (teacher signals less noisy)

---

# What It Changes Practically

Before:

* Siblings tightly clustered
* Cross-encoder does heavy lifting

After:

* Siblings moderately separated
* Cross-encoder focuses on fine-grained nuances

It reduces pressure on the reranking layer.

---

# Should You Add It Now or Later?

My recommendation:

Phase it in after:

* You train baseline MNR
* Measure sibling confusion rate

If confusion remains concentrated inside parent groups → enable hierarchy weighting.

No need to over-engineer v1.

---

# Final Answer

Yes — it aligns perfectly with your email-layer pipeline.

It strengthens the retrieval layer
without changing architecture
without increasing inference cost
and without complicating training loops.

---

If you want, next we can:

* Stress-test this against taxonomy changes
* Or simulate what happens when new sibling labels are added
* Or quantify expected accuracy lift from adding this

Your call.

Your move.
