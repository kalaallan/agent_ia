import re
import json


def safe_json_load(raw: str):
    try:
        return json.loads(raw)
    except Exception:
        # Cherche le premier [ et le dernier ] pour isoler la liste
        match = re.search(r"\[.*\]", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                return []
        return []
