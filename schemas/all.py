SYLLABUS_SCHEMA = {
    "type": "object",
    "properties": {
        "skills": {"type": "array", "items": {"type": "string"}, "minItems": 8, "maxItems": 14},
        "pitfalls": {"type": "array", "items": {"type": "string"}, "minItems": 5, "maxItems": 10},
    },
    "required": ["skills", "pitfalls"],
    "additionalProperties": False,
}

EXERCISE_AUTHOR_SCHEMA = {
    "type": "object",
    "properties": {
        "exercises": {
            "type": "array",
            "minItems": 8,
            "maxItems": 12,
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "section": {
                        "type": "string",
                        "enum": ["Warmup", "Core", "Proof", "Challenge"],
                    },
                    "title": {"type": "string"},
                    "statement": {"type": "string"},
                    "objective": {"type": "string"},
                    "uses": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["id", "section", "title", "statement", "objective", "uses"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["exercises"],
    "additionalProperties": False,
}

CALIBRATOR_SCHEMA = {
    "type": "object",
    "properties": {
        "timing": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "difficulty": {"type": "string", "enum": ["Routine", "Medium", "Exam", "Challenge"]},
                    "minutes": {"type": "integer", "minimum": 5, "maximum": 120},
                },
                "required": ["id", "difficulty", "minutes"],
                "additionalProperties": False,
            },
        },
        "total_minutes": {"type": "integer", "minimum": 10},
        "cuts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "reason": {"type": "string"},
                    "replacement": {"type": "string"},
                },
                "required": ["id", "reason", "replacement"],
                "additionalProperties": False,
            },
        },
        "revised_exercises": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Ordered list of exercise IDs to keep (can be unchanged).",
        },
    },
    "required": ["timing", "total_minutes", "cuts", "revised_exercises"],
    "additionalProperties": False,
}

SOLUTION_WRITER_SCHEMA = {
    "type": "object",
    "properties": {
        "solutions": {
            "type": "object",
            "additionalProperties": {"type": "string"},
            "description": "Map: exercise_id -> full solution text (not LaTeX, plain text ok).",
        }
    },
    "required": ["solutions"],
    "additionalProperties": False,
}

LATEX_PACKAGER_SCHEMA = {
    "type": "object",
    "properties": {
        "sheet_tex": {"type": "string"},
        "solutions_tex": {"type": "string"},
        "hints_tex": {"type": "string"},
    },
    "required": ["sheet_tex", "solutions_tex", "hints_tex"],
    "additionalProperties": False,
}

OFFICE_HOURS_SCHEMA = {
    "type": "object",
    "properties": {
        "guide_tex": {"type": "string"},
    },
    "required": ["guide_tex"],
    "additionalProperties": False,
}

REPAIR_SCHEMA = {
    "type": "object",
    "properties": {
        "patch": {"type": "object"},
        "notes": {"type": "string"},
    },
    "required": ["patch", "notes"],
    "additionalProperties": False,
}