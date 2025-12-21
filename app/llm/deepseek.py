import httpx
from typing import Optional

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-coder:1.3b"

async def generate_reply(
    prompt: str,
    temperature: float = 0.3,
    max_tokens: Optional[int] = None,
    timeout: int = 60
) -> str:
    """
    Generate a response using the DeepSeek-Coder model via Ollama.
    
    Args:
        prompt: The input prompt for the model
        temperature: Controls randomness (0.0 to 1.0)
        max_tokens: Maximum number of tokens to generate
        timeout: Request timeout in seconds
        
    Returns:
        Generated text response
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": max(0.1, min(1.0, temperature)),  # Clamp to 0.1-1.0
        },
    }
    
    if max_tokens:
        payload["options"]["num_predict"] = max(1, max_tokens)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            
        return data.get("response", "").strip()
    except httpx.HTTPStatusError as e:
        error_msg = f"Ollama API error: {e.response.status_code} - {e.response.text}"
        raise RuntimeError(error_msg) from e
    except Exception as e:
        raise RuntimeError(f"Failed to generate response: {str(e)}") from e
