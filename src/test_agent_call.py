from src.agent_call import call_json_schema

SCHEMA = {
    "type": "object",
    "properties": {
        "skills": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["skills"],
    "additionalProperties": False,
}

out = call_json_schema(
    system="You are a TA assistant. Output a short list of skills for this topic.",
    user_obj={"topic": "Cartan decomposition"},
    schema_name="skills_out",
    schema=SCHEMA,
)
print(out)
