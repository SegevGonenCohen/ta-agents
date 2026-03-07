from typing import Any, Dict, List, Optional
from src.logger import log
from src.local_verify import local_verify
from src.workers import (
    run_syllabus,
    run_exercises,
    run_calibrator,
    run_solutions,
    run_latex,
    run_office_hours,
    run_repair,
)


def deep_merge(dst: Dict[str, Any], patch: Dict[str, Any]) -> Dict[str, Any]:
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            deep_merge(dst[k], v)
        else:
            dst[k] = v
    return dst

def choose_worker(state: dict) -> str | None:
    """
    Deterministic replacement for the LLM manager.
    Returns the next worker name, or None if done.
    """

    syllabus = state.get("syllabus") or {}
    if not syllabus.get("skills") or not syllabus.get("pitfalls"):
        return "SYLLABUS_MAPPER"

    draft = state.get("draft") or {}
    exercises = draft.get("exercises")
    if not exercises:
        return "EXERCISE_AUTHOR"

    calibration = draft.get("calibration")
    if not calibration:
        return "CALIBRATOR"

    solutions = draft.get("solutions")
    if not solutions:
        return "SOLUTION_WRITER"

    artifacts = state.get("artifacts") or {}
    if not artifacts.get("sheet_tex") or not artifacts.get("solutions_tex") or not artifacts.get("hints_tex"):
        return "LATEX_PACKAGER"

    office = state.get("office_hours") or {}
    # depending on what you named it: guide_tex (new) or plan_md (old)
    if not office.get("guide_tex") and not office.get("plan_md"):
        return "OFFICE_HOURS"

    return None

def choose_top_issue(issues: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not issues:
        return None
    order = {"HIGH": 0, "MED": 1, "LOW": 2}
    return sorted(issues, key=lambda x: order.get(x["severity"], 3))[0]


def run_pipeline(state: Dict[str, Any], *, model: str, max_iters: int = 30) -> Dict[str, Any]:
    state.setdefault("history", [])
    state.setdefault("draft", {})
    state.setdefault("artifacts", {})
    state.setdefault("office_hours", {})
    
    log("=== PIPELINE START ===")

    for i in range(max_iters):
        log(f"--- Iteration {i+1} ---")

        log("Running LOCAL VERIFIER")
        v = local_verify(state)
        state["last_verify"] = v
        if v["pass"]:
            log("=== PIPELINE COMPLETE ===")
            state.setdefault("status", {})["phase"] = "done"
            return state
        else:
            log("VERIFIER: FAIL ✗")
            for issue in v.get("issues", []):
                log(f"  Issue: {issue['code']} ({issue['severity']})")
                
        worker = choose_worker(state)
        if worker is None:
            log("No remaining steps. Marking done.")
            state.setdefault("status", {})["phase"] = "done"
            return state

        log(f"Next worker: {worker}")
        state.setdefault("history", []).append({"worker": worker, "verify": v})

        if worker == "SYLLABUS_MAPPER":
            state["syllabus"] = run_syllabus(model, state)

        elif worker == "EXERCISE_AUTHOR":
            state["draft"]["exercises"] = run_exercises(model, state)["exercises"]

        elif worker == "CALIBRATOR":
            state["draft"]["calibration"] = run_calibrator(model, state)

            # Apply revised_exercises filter immediately (keep only selected IDs)
            keep = set(state["draft"]["calibration"]["revised_exercises"])
            state["draft"]["exercises"] = [ex for ex in state["draft"]["exercises"] if ex["id"] in keep]

        elif worker == "SOLUTION_WRITER":
            state["draft"]["solutions"] = run_solutions(model, state)["solutions"]

        elif worker == "LATEX_PACKAGER":
            out = run_latex(model, state)
            state["artifacts"]["sheet_tex"] = out["sheet_tex"]
            state["artifacts"]["solutions_tex"] = out["solutions_tex"]
            state["artifacts"]["hints_tex"] = out["hints_tex"]

        elif worker == "OFFICE_HOURS":
            log("Running OFFICE_HOURS")
            state["office_hours"]["guide_tex"] = run_office_hours(model, state)["guide_tex"]

        else:
            # fallback: targeted repair based on verifier
            top = choose_top_issue(v.get("issues", []))
            if top:
                state["status"] = {"phase": "forced_repair", "top_issue": top}
                rep = run_repair(model, state)
                deep_merge(state, rep["patch"])
            else:
                return state

    state.setdefault("status", {})["phase"] = "stopped_max_iters"
    return state