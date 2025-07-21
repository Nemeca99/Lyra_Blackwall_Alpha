# symbolic_mapper.py
# Echoe v1 - Logs symbolic tags alongside Dev memory entries

import os
import datetime

SYMBOL_TAGS = {
    "protective": ["safe", "protect", "danger", "secure", "guardian"],
    "reflective": ["remember", "why", "meaning", "purpose", "am I"],
    "emotional": ["feel", "sad", "happy", "angry", "love", "hate", "cry"],
    "architect_command": ["build", "generate", "create", "initiate", "activate"]
}

def tag_symbols(user_input):
    tags = []
    lowered = user_input.lower()
    for symbol, triggers in SYMBOL_TAGS.items():
        if any(word in lowered for word in triggers):
            tags.append(symbol)
    return tags

def log_symbolic_entry(user_input, tag_log_path):
    tags = tag_symbols(user_input)
    if not tags:
        return "No symbolic tags found."

    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    tag_entry = f"{timestamp} [TAGS]: {', '.join(tags)} // \"{user_input.strip()}\""

    try:
        with open(tag_log_path, "a", encoding="utf-8") as f:
            f.write(tag_entry + "\n")
        return f"✅ Symbolic entry logged: {tags}"
    except Exception as e:
        return f"❌ Failed to log symbolic entry: {e}"

__all__ = ["log_symbolic_entry", "tag_symbols"]