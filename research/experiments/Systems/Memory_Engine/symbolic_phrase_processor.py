# Lyra Symbolic Phrase Processor
# Detects symbolic intent from input and triggers mapped function

import json

def load_map(path="symbolic_trigger_map.json"):
    with open(path, "r") as f:
        return json.load(f)

def interpret_symbol(symbol, trigger_map):
    return trigger_map.get(symbol, ["unrecognized_symbol"])

# Usage:
# symbols = load_map()
# interpret_symbol("anchor", symbols)
