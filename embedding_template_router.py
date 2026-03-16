"""
EMBEDDING BASED TEMPLATE ROUTER
-------------------------------

Detects document template using embeddings
and routes to specialized extraction pipelines.
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# SIMPLE EMBEDDING FUNCTION
# ============================================================

def embed(text):

    # Replace with real embedding model
    # Example: OpenAI, SentenceTransformer

    return np.random.rand(384)


# ============================================================
# TEMPLATE DATABASE
# ============================================================

TEMPLATES = {
    "trade_confirmation": embed("trade confirmation counterparty settlement"),
    "email_instruction": embed("please process the following trade instruction"),
    "broker_statement": embed("statement account balance transaction summary")
}


# ============================================================
# TEMPLATE DETECTION
# ============================================================

def detect_template(document):

    doc_vec = embed(document)

    best = None
    best_score = -1

    for template in TEMPLATES:

        score = cosine_similarity(
            [doc_vec],
            [TEMPLATES[template]]
        )[0][0]

        if score > best_score:
            best_score = score
            best = template

    return best, best_score


# ============================================================
# ROUTING
# ============================================================

def route_document(document):

    template, score = detect_template(document)

    print(f"Detected template: {template} (score={score:.2f})")

    if template == "trade_confirmation":
        return "run_trade_pipeline"

    elif template == "email_instruction":
        return "run_email_pipeline"

    elif template == "broker_statement":
        return "run_statement_pipeline"

    return "run_generic_pipeline"


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    doc = """
TRADE CONFIRMATION

Trade ID: TRX-234234
Counterparty: JP Morgan
Settlement Date: 2024-02-14
"""

    pipeline = route_document(doc)

    print("Route to:", pipeline)
