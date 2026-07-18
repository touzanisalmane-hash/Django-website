"""
Small helper file that knows how to talk to a local Ollama server.

Ollama must be installed and running on your own computer for this to
work (see the README for setup instructions). By default Ollama listens
on http://127.0.0.1:11434.
"""
import os
import requests

# You can override these with environment variables if needed.
OLLAMA_HOST = os.environ.get('OLLAMA_HOST', 'http://127.0.0.1:11434')
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'llama3.2')

# How long (in seconds) we wait for Ollama to reply before giving up.
REQUEST_TIMEOUT = 60


def ask_ollama(messages):
    """
    Sends a conversation to the local Ollama server and returns the
    assistant's reply as plain text.

    `messages` is a list of dicts like:
        [{"role": "system", "content": "..."},
         {"role": "user", "content": "..."}]

    If Ollama isn't running, or the model hasn't been downloaded yet,
    we return a friendly error message instead of crashing the page.
    """
    url = f"{OLLAMA_HOST}/api/chat"
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
    }

    try:
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError:
        return (
            "I can't reach Ollama right now. Please make sure Ollama is "
            "installed and running on your computer (run `ollama serve` "
            "in a terminal), then try again."
        )
    except requests.exceptions.Timeout:
        return "The chatbot took too long to respond. Please try again."

    if response.status_code == 404:
        return (
            f"The model \"{OLLAMA_MODEL}\" isn't downloaded yet. "
            f"Run `ollama pull {OLLAMA_MODEL}` in a terminal, then try again."
        )

    if not response.ok:
        return f"Ollama returned an error (status {response.status_code}). Please try again."

    data = response.json()
    return data.get("message", {}).get("content", "").strip() or \
        "Sorry, I didn't get a response. Please try again."
