from typing import Any, Dict, List

def local_verify(state: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []

    syllabus = state.get("syllabus") or {}
    if not syllabus.get("skills"):
        issues.append({"code": "SYLLABUS_MISSING_SKILLS", "severity": "HIGH"})
    if not syllabus.get("pitfalls"):
        issues.append({"code": "SYLLABUS_MISSING_PITFALLS", "severity": "HIGH"})

    exercises = state.get("draft", {}).get("exercises")
    if not exercises:
        issues.append({"code": "EXERCISES_MISSING", "severity": "HIGH"})

    cal = state.get("draft", {}).get("calibration")
    if not cal:
        issues.append({"code": "CALIBRATION_MISSING", "severity": "HIGH"})

    sols = state.get("draft", {}).get("solutions")
    if not sols:
        issues.append({"code": "SOLUTIONS_MISSING", "severity": "HIGH"})

    art = state.get("artifacts", {})
    if not art.get("sheet_tex"):
        issues.append({"code": "ARTIFACT_SHEET_TEX_EMPTY", "severity": "HIGH"})
    if not art.get("solutions_tex"):
        issues.append({"code": "ARTIFACT_SOLUTIONS_TEX_EMPTY", "severity": "HIGH"})
    if not art.get("hints_tex"):
        issues.append({"code": "ARTIFACT_HINTS_TEX_EMPTY", "severity": "HIGH"})

    oh = state.get("office_hours", {})
    if not oh.get("guide_tex") and not oh.get("plan_md"):
        issues.append({"code": "OFFICE_HOURS_MISSING", "severity": "MED"})

    return {"pass": len(issues) == 0, "issues": issues}