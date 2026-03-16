import re

def extract_kv(markdown):

    data = {}
    current_key = None

    lines = markdown.splitlines()

    for line in lines:

        line = line.strip()

        # skip page markers
        if re.match(r'^\s*(page\s*\d+|---.*---)\s*$', line, re.I):
            continue

        # detect new key
        match = re.match(r'^([A-Za-z0-9 /()\-]+):\s*(.*)$', line)

        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()

            data[key] = value
            current_key = key

        else:
            # continuation of previous field
            if current_key and line:
                data[current_key] += " " + line

    return data
