import requests
from backend.config import LMSTUDIO_API_URL

def ask_local(question: str, context: str = ""):
    payload = {
        "model": "local",
        "messages": [
            {"role": "system", "content": "Use the given context for accuracy"},
            {"role": "user", "content": f"{context}\n\nQuestion: {question}"}
        ]
    }

    r = requests.post(LMSTUDIO_API_URL, json=payload)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]