import json
from typing import Any, Dict, Optional

from src.logger import log
from src.config import DEFAULT_MODEL
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def call_json_schema(
    *,
    model: Optional[str] = None,
    system: str,
    user_obj: Dict[str, Any],
    schema_name: str,
    schema: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Compatible fallback: uses chat.completions with JSON mode.
    Ensures output is valid JSON, then validates against the provided JSON Schema locally.
    """
    model = model or DEFAULT_MODEL
    # 1) Ask for JSON object output
    log(f"CALL → {schema_name}") # Human added
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": (
                    "Return JSON only.\n"
                    "Your JSON MUST validate against this JSON Schema:\n"
                    f"{json.dumps(schema)}\n\n"
                    "Here is the input object:\n"
                    f"{json.dumps(user_obj)}"
                ),
            },
        ],
        response_format={"type": "json_object"},
    )

    text = resp.choices[0].message.content
    data = json.loads(text)
    
    log(f"DONE ← {schema_name}") # Human added

    # 2) Validate locally against schema (strictness restored)
    try:
        import jsonschema
        jsonschema.validate(instance=data, schema=schema)
    except Exception as e:
        # Raise a clear error so you can see what broke
        raise RuntimeError(
            f"{schema_name} output failed schema validation: {e}\n\nModel output:\n{text}"
        )

    return data