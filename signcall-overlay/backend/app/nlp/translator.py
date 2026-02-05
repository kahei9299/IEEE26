from app import settings
from app.recognition.phrase_set import PHRASES
from app.nlp.templates import TEMPLATES
from app.nlp.llm_client import gloss_to_english

def translate(pred: dict, profile: dict) -> dict:
    token = pred["token"]
    conf = float(pred["confidence"])
    top2 = pred.get("top2", [token])
    style = profile.get("style", "concise")

    gloss = PHRASES.get(token, {}).get("gloss", token)

    # Low confidence -> ask clarification
    if conf < settings.CONF_MED:
        alt = top2[1] if len(top2) > 1 else token
        return {
            "caption": f"Unclear — did you mean {token} or {alt}?",
            "mode": "uncertain",
            "confidence": conf
        }

    # Medium confidence -> template
    if conf < settings.CONF_HIGH:
        return {
            "caption": TEMPLATES.get(token, gloss),
            "mode": "template",
            "confidence": conf
        }

    # High confidence -> try LLM polish, fallback to template
    llm = gloss_to_english(gloss, style=style)
    if llm:
        return {"caption": llm, "mode": "llm", "confidence": conf}

    return {"caption": TEMPLATES.get(token, gloss), "mode": "template", "confidence": conf}
