from typing import Any, Dict
from src.agent_call import call_json_schema
from schemas.all import (
    SYLLABUS_SCHEMA,
    EXERCISE_AUTHOR_SCHEMA,
    CALIBRATOR_SCHEMA,
    SOLUTION_WRITER_SCHEMA,
    LATEX_PACKAGER_SCHEMA,
    OFFICE_HOURS_SCHEMA,
    REPAIR_SCHEMA,
)
from prompts.prompts import (
    SYLLABUS_SYS,
    EXERCISE_AUTHOR_SYS,
    CALIBRATOR_SYS,
    SOLUTION_WRITER_SYS,
    LATEX_PACKAGER_SYS,
    OFFICE_HOURS_SYS,
    REPAIR_SYS,
)


def run_syllabus(model: str, state: Dict[str, Any]) -> Dict[str, Any]:
    return call_json_schema(
        model=model,
        system=SYLLABUS_SYS,
        user_obj={"course": state["course"], "style_guide": state.get("style_guide")},
        schema_name="syllabus_out",
        schema=SYLLABUS_SCHEMA,
    )


def run_exercises(model: str, state: Dict[str, Any]) -> Dict[str, Any]:
    return call_json_schema(
        model=model,
        system=EXERCISE_AUTHOR_SYS,
        user_obj={
            "course": state["course"],
            "syllabus": state["syllabus"],
            "style_guide": state.get("style_guide"),
        },
        schema_name="exercise_author_out",
        schema=EXERCISE_AUTHOR_SCHEMA,
    )


def run_calibrator(model: str, state: Dict[str, Any]) -> Dict[str, Any]:
    return call_json_schema(
        model=model,
        system=CALIBRATOR_SYS,
        user_obj={
            "course": state["course"],
            "draft": {"exercises": state["draft"]["exercises"]},
        },
        schema_name="calibrator_out",
        schema=CALIBRATOR_SCHEMA,
    )


def run_solutions(model: str, state: Dict[str, Any]) -> Dict[str, Any]:
    return call_json_schema(
        model=model,
        system=SOLUTION_WRITER_SYS,
        user_obj={
            "course": state["course"],
            "draft": {
                "exercises": state["draft"]["exercises"],
                "calibration": state["draft"]["calibration"],
            },
        },
        schema_name="solution_writer_out",
        schema=SOLUTION_WRITER_SCHEMA,
    )


def run_latex(model: str, state: Dict[str, Any]) -> Dict[str, Any]:
    return call_json_schema(
        model=model,
        system=LATEX_PACKAGER_SYS,
        user_obj={
            "course": state["course"],
            "draft": state["draft"],
            "style_guide": state.get("style_guide"),
        },
        schema_name="latex_packager_out",
        schema=LATEX_PACKAGER_SCHEMA,
    )


def run_office_hours(model: str, state: Dict[str, Any]) -> Dict[str, Any]:
    return call_json_schema(
        model=model,
        system=OFFICE_HOURS_SYS,
        user_obj={
            "course": state["course"],
            "syllabus": state["syllabus"],
            "draft": {
                "exercises": state["draft"]["exercises"],
                "calibration": state["draft"].get("calibration"),
            },
            "style_guide": state.get("style_guide"),
        },
        schema_name="office_hours_out",
        schema=OFFICE_HOURS_SCHEMA,
    )

def run_repair(model: str, state: Dict[str, Any]) -> Dict[str, Any]:
    return call_json_schema(
        model=model,
        system=REPAIR_SYS,
        user_obj={"state": state, "issues": state.get("last_verify", {}).get("issues", [])},
        schema_name="repair_out",
        schema=REPAIR_SCHEMA,
    )