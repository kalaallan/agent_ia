from app.utils.gemini_utils import call_gemini_multimodal
from app.utils.json_utils import safe_json_load


def process_document(file_bytes: bytes, max_iterations=10):
    """
    Iterative extraction:
    - 1 exercise per call
    - avoids duplicates
    """

    all_results = []
    seen_statements = []

    for i in range(max_iterations):

        print(f"\n[DEBUG] Iteration {i+1}")

        prompt = f"""
# ROLE
You are an expert teacher.

# TASK
Extract ONLY ONE new exercise from the document.

# RULES
- Do NOT return exercises already listed below
- If no new exercise exists, return []

# ALREADY FOUND:
{seen_statements}

# OUTPUT FORMAT
[
  {{
    "type": "exercice | question | problématique",
    "hint": ["...", "...", "..."],
    "solution": "..."
  }}
]
"""

        try:
            raw = call_gemini_multimodal(file_bytes, prompt)

            print("[DEBUG] RAW:", raw)

            parsed = safe_json_load(raw)

            if not parsed:
                print("[DEBUG] No more exercises found -> stopping")
                break

            exercise = parsed[0]

            signature = exercise.get("solution", "")[:1000]

            if signature in seen_statements:
                print("[DEBUG] Duplicate detected -> stopping")
                break

            seen_statements.append(signature)
            all_results.append(exercise)

        except Exception as e:
            print("[ERROR]", str(e))
            break

    print("\n[DEBUG] FINAL RESULT:", all_results)

    return all_results
