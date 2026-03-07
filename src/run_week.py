import os
import yaml
from dotenv import load_dotenv

from src.orchestrator import run_pipeline
from src.pdf_notes import extract_notes
from src.config import DEFAULT_MODEL


def main():
    load_dotenv()

    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY not set. "
            "Add it to a .env file in the project root (see README)."
        )

    config_path = os.environ.get("TA_CONFIG", "inputs/week.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    state = {
        "course": cfg["course"],
        "style_guide": cfg.get("style_guide"),
        "syllabus": None,
        "draft": {},
        "artifacts": {},
        "office_hours": {},
        "status": {"phase": "start"},
    }

    pdf_path = "inputs/notes.pdf"
    pages = cfg["course"].get("notes_pages")

    if pages:
        notes_text = extract_notes(pdf_path, pages)
        state["course"]["notes_text"] = notes_text

    template_path = "inputs/template.tex"
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()

        if state.get("style_guide") is None:
            state["style_guide"] = {}

        state["style_guide"]["template_tex"] = template

    model = DEFAULT_MODEL
    out_state = run_pipeline(state, model=model, max_iters=cfg.get("max_iters", 30))

    os.makedirs("out", exist_ok=True)
    with open("out/sheet.tex", "w", encoding="utf-8") as f:
        f.write(out_state["artifacts"]["sheet_tex"])
    with open("out/solutions.tex", "w", encoding="utf-8") as f:
        f.write(out_state["artifacts"]["solutions_tex"])
    with open("out/hints.tex", "w", encoding="utf-8") as f:
        f.write(out_state["artifacts"]["hints_tex"])
    with open("out/exercise_class_guide.tex", "w", encoding="utf-8") as f:
        f.write(out_state["office_hours"]["guide_tex"])

    # Optional: dump state for debugging
    with open("out/state.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(out_state, f, sort_keys=False, allow_unicode=True)

    print("Wrote: out/sheet.tex, out/solutions.tex, out/hints.tex, out/exercise_class_guide.tex")


if __name__ == "__main__":
    main()
