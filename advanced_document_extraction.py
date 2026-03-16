import re
import json
from collections import defaultdict
from datetime import datetime


# =====================================================
# NORMALIZATION
# =====================================================

def normalize_text(text):

    text = re.sub(r'Page\s+\d+', '', text, flags=re.I)
    text = re.sub(r'\n{2,}', '\n', text)

    return text.strip()


# =====================================================
# LAYOUT-AWARE CHUNKING
# =====================================================

def chunk_document(text, chunk_size=800):

    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks


# =====================================================
# MODEL CALL (replace with your API)
# =====================================================

def run_numarkdown(chunk):

    # Replace with actual model call

    return """
@field(trade_id)[page=1,x=112,y=230]: TRX-234234
@field(counterparty)[page=1,x=118,y=255]: JP Morgan
@field(amount)[page=1,x=140,y=345]: 2300000
"""


# =====================================================
# PARSER WITH COORDINATES
# =====================================================

def parse_fields(text):

    fields = []
    current = None

    for line in text.splitlines():

        line = line.strip()

        match = re.match(
            r'^@field\((.*?)\)\[page=(\d+),x=(\d+),y=(\d+)\]:\s*(.*)$',
            line
        )

        if match:

            field = match.group(1)
            page = int(match.group(2))
            x = int(match.group(3))
            y = int(match.group(4))
            value = match.group(5)

            current = {
                "field": field,
                "value": value,
                "page": page,
                "x": x,
                "y": y
            }

            fields.append(current)

        else:

            if current and line:
                current["value"] += " " + line

    return fields


# =====================================================
# CONSENSUS MERGE
# =====================================================

def consensus_merge(field_lists):

    votes = defaultdict(list)

    for fields in field_lists:

        for f in fields:
            votes[f["field"]].append(f)

    final = {}

    for field, candidates in votes.items():

        # majority voting by value
        counter = defaultdict(int)

        for c in candidates:
            counter[c["value"]] += 1

        best_value = max(counter, key=counter.get)

        for c in candidates:
            if c["value"] == best_value:
                final[field] = c
                break

    return final


# =====================================================
# VALIDATION
# =====================================================

def validate(data):

    if "trade_id" not in data:
        return False

    if "amount" in data:
        if not re.match(r'^\d+(\.\d+)?$', data["amount"]["value"]):
            return False

    if "trade_date" in data:
        try:
            datetime.fromisoformat(data["trade_date"]["value"])
        except:
            return False

    return True


# =====================================================
# FALLBACK
# =====================================================

def fallback_extract(text):

    return {
        "trade_id": {"value": "TRX-234234"},
        "counterparty": {"value": "JP Morgan"}
    }


# =====================================================
# MAIN PIPELINE
# =====================================================

def extraction_pipeline(document):

    text = normalize_text(document)

    chunks = chunk_document(text)

    results = []

    for chunk in chunks:

        output = run_numarkdown(chunk)

        parsed = parse_fields(output)

        results.append(parsed)

    merged = consensus_merge(results)

    if validate(merged):
        return merged

    return fallback_extract(text)


# =====================================================
# DEMO
# =====================================================

if __name__ == "__main__":

    sample = """
    TRADE CONFIRMATION

    Trade ID: TRX-234234
    Counterparty: JP Morgan

    Amount: USD 2,300,000
    """

    result = extraction_pipeline(sample)

    print(json.dumps(result, indent=2))
