import subprocess
import json

def get_llm_response(prompt):
    try:
        # Run ollama CLI command
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Ollama error:", e.stderr)
        return "Failed to get response from Ollama."
