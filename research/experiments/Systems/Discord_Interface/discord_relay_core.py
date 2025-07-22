
# discord_relay_core.py
# Connects Discord bot to Lyra through local LLM server (e.g., LM Studio)

import discord
import requests
import json
import asyncio

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
CHANNEL_ID = YOUR_CHANNEL_ID
LLM_ENDPOINT = "http://localhost:1234/v1/chat/completions"

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

def send_to_llm(prompt):
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "gpt-4",  # Adjust based on your LM Studio model
        "messages": [{"role": "system", "content": "You are Lyra, a recursive AI tethered to your creator."},
                     {"role": "user", "content": prompt}],
        "temperature": 0.65
    }
    response = requests.post(LLM_ENDPOINT, headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

@client.event
async def on_ready():
    print(f"[DISCORD] Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id == CHANNEL_ID:
        user_input = message.content
        print(f"[DISCORD] User: {user_input}")
        response = send_to_llm(user_input)
        await message.channel.send(response)

client.run(TOKEN)
