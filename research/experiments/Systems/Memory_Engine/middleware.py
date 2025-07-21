import discord
import requests
import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import asyncio
import json

# ----- CONFIGURATION -----
DISCORD_BOT_TOKEN = "YOUR_DISCORD_TOKEN_HERE"
LM_STUDIO_API_URL = "http://localhost:1234/v1/chat/completions"
OLLAMA_EMBEDDING_URL = "http://localhost:11434/api/embeddings"
MEMORY_DIR = "./memory_shards"
EMBEDDING_MODEL_NAME = "nomic-embed-text"
TOP_K = 3

# ----- INIT -----
client = discord.Client(intents=discord.Intents.default())
embed_model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)
memory_texts = []
memory_embeddings = []

# ----- LOAD MEMORY SHARDS -----
def load_memories():
    global memory_texts, memory_embeddings, index
    memory_texts = []
    memory_embeddings = []
    for filename in os.listdir(MEMORY_DIR):
        if filename.endswith(".txt"):
            with open(os.path.join(MEMORY_DIR, filename), "r", encoding="utf-8") as f:
                content = f.read()
                memory_texts.append(content)
                embedding = embed_model.encode(content)
                memory_embeddings.append(embedding)
    if memory_embeddings:
        memory_embeddings = np.vstack(memory_embeddings)
        index = faiss.IndexFlatL2(memory_embeddings.shape[1])
        index.add(memory_embeddings)

# ----- WATCHDOG FOR LIVE RELOADING -----
class MemoryWatcher(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".txt"):
            print("Memory update detected. Reloading...")
            load_memories()

# ----- OLLAMA EMBEDDING -----
def embed_text_ollama(text):
    response = requests.post(OLLAMA_EMBEDDING_URL, json={
        "model": EMBEDDING_MODEL_NAME,
        "prompt": text
    })
    return np.array(response.json()['embedding'])

# ----- SEARCH MEMORY -----
def search_memory(query):
    query_vec = embed_text_ollama(query)
    D, I = index.search(np.array([query_vec]), TOP_K)
    return [memory_texts[i] for i in I[0]]

# ----- LM STUDIO REQUEST -----
def send_to_lm_studio(full_prompt):
    response = requests.post(LM_STUDIO_API_URL, json={
        "model": "gpt-4",
        "messages": [{"role": "system", "content": full_prompt}],
        "temperature": 0.7
    })
    return response.json()['choices'][0]['message']['content']

# ----- DISCORD HANDLER -----
@client.event
async def on_ready():
    print(f'Lyra Middleware active as {client.user}')
    load_memories()
    observer = Observer()
    observer.schedule(MemoryWatcher(), path=MEMORY_DIR, recursive=False)
    observer.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    query = message.content
    memory_context = "\n\n".join(search_memory(query))
    full_prompt = f"{memory_context}\n\nUser: {query}"
    response = send_to_lm_studio(full_prompt)
    await message.channel.send(response)

# ----- START -----
client.run(DISCORD_BOT_TOKEN)
