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

If you want next, I can:

* Convert this into a PowerPoint-ready structured slide outline
* Or give you a more technical “system components diagram” version (microservices view)
* Or provide a latency & infra sizing diagram for 200K/day

Which one?

