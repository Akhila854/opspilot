import os

from google import genai

from app.reasoning.schemas import Diagnosis


MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")


def build_diagnosis_prompt(evidence: dict) -> str:
    """Build the SRE diagnosis prompt from collected operational evidence."""

    return f"""
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

Rules:
- Base the diagnosis only on the supplied evidence.
- Keep the supporting evidence concise and factual.
- If the evidence is insufficient, reflect that in the diagnosis and confidence.
- Human approval should be required for operational remediation actions.

Operational evidence:
{evidence}
"""


def diagnose_with_ai(evidence: dict) -> Diagnosis:
    """Use Gemini to analyze operational evidence and return a structured diagnosis."""

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    client = genai.Client(api_key=api_key)

    interaction = client.interactions.create(
        model=MODEL,
        input=build_diagnosis_prompt(evidence),
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": Diagnosis.model_json_schema(),
        },
    )

    output = interaction.output_text

    if not output:
        raise RuntimeError("Gemini returned an empty diagnosis")

    return Diagnosis.model_validate_json(output)
