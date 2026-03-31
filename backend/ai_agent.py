import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def get_ai_fix(issue):
    prompt = f"""
    You are a cloud security expert.

    Issue: {issue['title']}
    Severity: {issue['severity']}

    Explain the risk and give a Terraform fix in 2-3 lines.
    """

    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    data = response.json()
    return data.get("response", "No response from AI")