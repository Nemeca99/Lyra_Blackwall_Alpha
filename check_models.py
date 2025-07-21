import requests

try:
    r = requests.get('http://localhost:11434/api/tags')
    models = r.json()
    print('Available Ollama models:')
    for model in models.get('models', []):
        print(f'  - {model["name"]}')
except Exception as e:
    print(f'Error: {e}') 