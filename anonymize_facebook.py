"""
anonymize_facebook.py

Purpose:
- Clean and anonymize Facebook JSON messages for safe use in quizzes or LLMs.

Input:
- Facebook JSON export file (e.g., messages.json)

Output:
- cleaned_messages.json → anonymized messages
- name_mapping.json → anonymized names mapping

Format of cleaned_messages.json:
[
  {
    "speaker": "Friend_A",
    "text": "Hello, how are you?",
    "timestamp_ms": 1602342342342
  }
]

Usage Notes:
- Replaces sender names and mentions inside text.
- Removes reactions and sensitive info (emails, phone numbers, URLs).
- Prompt example for ChatGPT:
  "Generate a quiz where participants guess who said each message. Use only the anonymized messages."
"""

import json
import re
from collections import defaultdict

# ---- CONFIG ----
INPUT_FILE = "messages.json"   # your Facebook export JSON
OUTPUT_FILE = "cleaned_messages.json"
MAPPING_FILE = "name_mapping.json"
MY_REAL_NAME = "Your name" # Your real name on Facebook
ME_NAME = "Me"
# -----------------

REACTION_PATTERN = re.compile(
    r"^(reacted|liked|loved|laughed|wow'ed|wowed|sad|angry).*", 
    re.IGNORECASE
)

def clean_text(text, speaker_map):
    """Clean text and replace all real names with anonymized labels safely."""
    if not isinstance(text, str):
        return ""

    t = text.strip()

    # Remove reaction lines
    t_lower = t.lower()
    if "reacted" in t_lower and "message" in t_lower:
        return ""
    if t.startswith("ð"):
        return ""

    # Remove emails
    t = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[email_removed]", t)

    # Remove phone numbers
    t = re.sub(r"\b\+?\d[\d\s\-().]{6,}\b", "[phone_removed]", t)

    # Remove URLs
    t = re.sub(r"https?://\S+", "[link_removed]", t)

    # Replace mentions of real names safely
    for real_name, anon_name in speaker_map.items():
        if not real_name.strip():
            continue

        # Replace full name
        try:
            pattern = re.compile(re.escape(real_name), re.IGNORECASE)
            t = pattern.sub(anon_name, t)
        except re.error:
            pass  # skip any problematic names

        # Replace first/last names individually
        parts = real_name.split()
        for p in parts:
            if not p.strip():
                continue
            try:
                pattern = re.compile(r'\b' + re.escape(p) + r'\b', re.IGNORECASE)
                t = pattern.sub(anon_name, t)
            except re.error:
                continue  # skip this part if it breaks regex

    return t.strip()

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    messages = data.get("messages", data)

    speaker_map = {}
    speaker_counter = 0

    cleaned = []

    for msg in messages:
        sender = msg.get("sender_name", "").strip()
        text = msg.get("content", "")

        # Skip empty or non-text messages
        if not text or not isinstance(text, str):
            continue

        # Clean text and skip if empty (e.g. removed reaction messages)
        cleaned_text = clean_text(text, speaker_map)
        if not cleaned_text:
            continue

        # Assign anonymized names
        if sender not in speaker_map:
            if sender.lower() == MY_REAL_NAME.lower():
                speaker_map[sender] = ME_NAME
            else:
                speaker_map[sender] = f"Friend_{chr(65 + speaker_counter)}"
                speaker_counter += 1

        clean_msg = {
            "speaker": speaker_map[sender],
            "text": cleaned_text,
            "timestamp_ms": msg.get("timestamp_ms", None)
        }

        cleaned.append(clean_msg)

    # Save cleaned messages
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    # Save mapping between anonymized and real names
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(speaker_map, f, indent=2, ensure_ascii=False)

    print(f"Done! Saved {len(cleaned)} messages to {OUTPUT_FILE}")
    print(f"Name mapping saved to {MAPPING_FILE}")


if __name__ == "__main__":
    main()
