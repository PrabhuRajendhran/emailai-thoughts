"""
High-Accuracy Document Extraction Pipeline
------------------------------------------

Pipeline:
Document
  → nuMarkdown structured extraction
  → deterministic parser
  → schema validation
  → optional nuExtract fallback

Designed for large-scale document processing.
"""

import re
import json
from datetime import datetime


# ============================================================
# PROMPT FOR nuMarkdown-8-thinking
# ============================================================

NUMARKDOWN_PROMPT = """
You are converting a document into structured fields for deterministic parsing.

STRICT OUTPUT RULES:

1. Output ONLY structured fields.
2. Each field must follow this exact format:

@field(field_name): value

3. If the value spans multiple lines, continue writing on the next line.
4. Do NOT repeat field tags for continuation lines.
5. Do NOT paraphrase values.
6. Do NOT hallucinate fields.
7. Ignore page numbers, headers, and footers.

CANONICAL FIELDS:

trade_id
counterparty
trade_date
settlement_date
currency
amount
instrument
description

EXAMPLE OUTPUT:

@field(trade_id): TRX-234234
@field(counterparty): JP Morgan
@field(trade_date): 2024-02-12
@field(settlement_date): 2024-02-14
@field(currency): USD
@field(amount): 2300000
@field(instrument): Equity Swap
@field(description):
This structured equity swap was executed
between counterparties under ISDA agreement
and settles via Euroclear.

Only output structured fields.
"""


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:
    """
    Removes page artifacts and normalizes whitespace.
    """

    text = re.sub(r'Page\s+\d+', '', text, flags=re.I)
    text = re.sub(r'---+\s*Page.*', '', text, flags=re.I)
    text = re.sub(r'\n{2,}', '\n', text)

    return text.strip()


# ============================================================
# STRUCTURED FIELD PARSER
# ============================================================

def parse_structured_fields(text: str) -> dict:
    """
    Parses @field(field_name): value format.
    Handles multi-line values automatically.
    """

    data = {}
    current_field = None

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        match = re.match(r'^@field\((.*?)\):\s*(.*)$', line)

        if match:

            field = match.group(1).strip()
            value = match.group(2).strip()

            data[field] = value
            current_field = field

        else:
            if current_field and line:
                data[current_field] += " " + line

    return data


# ============================================================
# SCHEMA VALIDATION
# ============================================================

def validate_schema(data: dict) -> bool:
    """
    Validates extracted fields.
    """

    required = ["trade_id", "counterparty"]

    for field in required:
        if field not in data:
            return False

    if "trade_date" in data:
        try:
            datetime.fromisoformat(data["trade_date"])
        except:
            return False

    if "settlement_date" in data:
        try:
            datetime.fromisoformat(data["settlement_date"])
        except:
            return False

    if "amount" in data:
        if not re.match(r'^\d+(\.\d+)?$', data["amount"]):
            return False

    return True


# ============================================================
# MODEL CALLS (REPLACE WITH YOUR API)
# ============================================================

def run_numarkdown(document_text: str) -> str:
    """
    Call nuMarkdown-8-thinking model.

    Replace with your actual API call.
    """

    print("Running nuMarkdown extraction...")

    # Example stub output
    return """
@field(trade_id): TRX-234234
@field(counterparty): JP Morgan
@field(trade_date): 2024-02-12
@field(settlement_date): 2024-02-14
@field(currency): USD
@field(amount): 2300000
@field(instrument): Equity Swap
@field(description):
This structured equity swap was executed
between counterparties under ISDA agreement
and settles via Euroclear.
"""


def run_nuextract(document_text: str) -> dict:
    """
    Fallback extraction model.
    """

    print("Fallback to nuExtract...")

    return {
        "trade_id": "TRX-234234",
        "counterparty": "JP Morgan",
        "amount": "2300000"
    }


# ============================================================
# EXTRACTION PIPELINE
# ============================================================

def extraction_pipeline(document_text: str) -> dict:

    # Step 1 normalize
    normalized = normalize_text(document_text)

    # Step 2 run nuMarkdown
    markdown_output = run_numarkdown(normalized)

    # Step 3 parse structured fields
    parsed = parse_structured_fields(markdown_output)

    # Step 4 validate schema
    if validate_schema(parsed):
        print("Extraction succeeded via deterministic parsing.")
        return parsed

    # Step 5 fallback
    fallback = run_nuextract(normalized)

    return fallback


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    sample_document = """
    TRADE CONFIRMATION

    Trade ID: TRX-234234
    Counterparty: JP Morgan

    Trade Date: 2024-02-12
    Settlement Date: 2024-02-14

    Instrument: Equity Swap
    Amount: USD 2,300,000

    Description:
    This structured equity swap was executed under ISDA agreement
    between the counterparties and settles via Euroclear.
    """

    result = extraction_pipeline(sample_document)

    print("\nFINAL OUTPUT\n")
    print(json.dumps(result, indent=2))
