import os

from google import genai

from app.reasoning.schemas import Diagnosis


MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")


def diagnose_with_ai(evidence: dict) -> Diagnosis:
    """Use Gemini to analyze operational evidence and return a structured diagnosis."""

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an SRE incident diagnosis assistant.

Analyze ONLY the supplied operational evidence.
Do not invent facts or evidence.

Determine:
- the most likely root cause
- severity
- confidence from 0 to 1
- supporting evidence
- recommended next operational action
- whether human approval is required before taking action

Operational evidence:
{evidence}
"""

    interaction = client.interactions.create(
        model=MODEL,
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": Diagnosis.model_json_schema(),
        },
    )

    return Diagnosis.model_validate_json(interaction.output_text)
