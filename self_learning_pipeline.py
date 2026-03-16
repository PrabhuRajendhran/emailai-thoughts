"""
SELF LEARNING DOCUMENT EXTRACTION PIPELINE
------------------------------------------

Capabilities
- structured extraction
- deterministic parsing
- schema validation
- alias discovery
- prompt learning
"""

import re
import json
import os
from datetime import datetime


# ============================================================
# CONFIG
# ============================================================

ALIAS_FILE = "alias_store.json"

CANONICAL_FIELDS = [
    "trade_id",
    "counterparty",
    "trade_date",
    "settlement_date",
    "currency",
    "amount",
    "instrument",
    "description"
]


# ============================================================
# LOAD / SAVE ALIAS STORE
# ============================================================

def load_alias_store():

    if os.path.exists(ALIAS_FILE):

        with open(ALIAS_FILE) as f:
            return json.load(f)

    alias_map = {f: [] for f in CANONICAL_FIELDS}

    save_alias_store(alias_map)

    return alias_map


def save_alias_store(data):

    with open(ALIAS_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(text):

    text = re.sub(r'Page\s+\d+', '', text, flags=re.I)
    text = re.sub(r'\n{2,}', '\n', text)

    return text.strip()


# ============================================================
# PROMPT BUILDER
# ============================================================

def build_prompt(alias_map):

    prompt = """
Extract structured fields from the document.

Output format:

@field(field_name): value

Canonical fields and aliases:
"""

    for field in alias_map:

        prompt += f"\n{field} : {', '.join(alias_map[field])}"

    return prompt


# ============================================================
# MODEL STUB
# ============================================================

def run_numarkdown(text):

    # Replace with real LLM call

    return """
@field(trade_id): TRX-99232
@field(counterparty): Goldman Sachs
@field(amount): 5000000
"""


# ============================================================
# PARSER
# ============================================================

def parse_fields(text):

    data = {}
    current = None

    for line in text.splitlines():

        line = line.strip()

        m = re.match(r'^@field\((.*?)\):\s*(.*)$', line)

        if m:

            field = m.group(1)
            value = m.group(2)

            data[field] = value
            current = field

        else:

            if current and line:
                data[current] += " " + line

    return data


# ============================================================
# VALIDATION
# ============================================================

def validate(data):

    if "trade_id" not in data:
        return False

    if "amount" in data:
        if not re.match(r'^\d+(\.\d+)?$', data["amount"]):
            return False

    if "trade_date" in data:
        try:
            datetime.fromisoformat(data["trade_date"])
        except:
            return False

    return True


# ============================================================
# ALIAS DISCOVERY
# ============================================================

def discover_aliases(text, alias_map):

    discovered = []

    lines = text.lower().splitlines()

    for line in lines:

        if ":" not in line:
            continue

        label = line.split(":")[0].strip()

        known = False

        for field in alias_map:

            if label == field or label in alias_map[field]:
                known = True

        if not known:
            discovered.append(label)

    return discovered


# ============================================================
# UPDATE ALIAS STORE
# ============================================================

def update_alias_store(alias_map, new_aliases):

    for alias in new_aliases:

        print(f"New alias discovered: {alias}")

        # simple heuristic mapping
        if "transaction" in alias:
            alias_map["trade_id"].append(alias)

        elif "cpty" in alias:
            alias_map["counterparty"].append(alias)

        elif "notional" in alias:
            alias_map["amount"].append(alias)

    save_alias_store(alias_map)


# ============================================================
# PIPELINE
# ============================================================

def extraction_pipeline(document):

    alias_map = load_alias_store()

    normalized = normalize_text(document)

    prompt = build_prompt(alias_map)

    model_output = run_numarkdown(normalized)

    parsed = parse_fields(model_output)

    if validate(parsed):

        print("Extraction success")

        return parsed

    print("Extraction failed — learning...")

    new_aliases = discover_aliases(normalized, alias_map)

    update_alias_store(alias_map, new_aliases)

    return parsed


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    doc = """
Transaction Reference: TRX-99232
CPTY: Goldman Sachs
Notional: 5000000
"""

    result = extraction_pipeline(doc)

    print(json.dumps(result, indent=2))
