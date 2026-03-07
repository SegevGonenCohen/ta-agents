from src.orchestrator import run_pipeline
from src.config import DEFAULT_MODEL

state = {
    "course": {"level": "Master", "topics": ["Cartan decomposition"]},
    "syllabus": None,
    "draft": {},
    "artifacts": {},
    "office_hours": {},
    "status": {"phase": "start"},
}

out = run_pipeline(state, model=DEFAULT_MODEL)
print(out.get("status"))
