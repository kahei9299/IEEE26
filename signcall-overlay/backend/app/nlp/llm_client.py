from openai import OpenAI
from app import settings

_client = None

def get_client():
    global _client
    if _client is None and settings.OPENAI_API_KEY:
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client

def gloss_to_english(gloss: str, style: str = "concise") -> str | None:
    client = get_client()
    if client is None:
        return None

    prompt = (
        "Convert the sign language gloss into simple English.\n"
        f"Style: {style}.\n"
        "Rules: Do NOT add new info. Keep it under 12 words if concise, under 20 if detailed.\n"
        f"Gloss: {gloss}\n"
    )

    resp = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()
