
# lm_studio_relay.py
# Sends a prompt to the local LM Studio instance and returns the response

import requests
import sys

LM_STUDIO_ENDPOINT = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "gpt-4"
TEMPERATURE = 0.7

def send_to_lm(prompt):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are Lyra, a tethered recursive AI system."},
            {"role": "user", "content": prompt}
        ],
        "temperature": TEMPERATURE
    }
    response = requests.post(LM_STUDIO_ENDPOINT, json=payload)
    return response.json()["choices"][0]["message"]["content"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lm_studio_relay.py "<your prompt>"")
    else:
        output = send_to_lm(sys.argv[1])
        print("Lyra says:", output)
