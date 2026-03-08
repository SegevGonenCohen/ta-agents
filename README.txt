TA-Agents Exercise Sheet Generator
==================================

This tool uses an LLM pipeline to generate weekly exercise
materials from a small configuration file and lecture notes.

It produces four LaTeX documents:

  - Exercise sheet (problems only)
  - Full solutions
  - Hints sheet
  - A teaching guide for an exercise class (configurable length)

--------------------------------------------------

SETUP (first time)

1. Install Python 3.10+

2. Create and activate a virtual environment

   python -m venv .venv
   source .venv/bin/activate          # macOS / Linux
   .venv\Scripts\activate             # Windows

3. Install required packages

   pip install -r requirements.txt

4. Add your OpenAI API key

   Create a file called .env in the project root containing:

       OPENAI_API_KEY=sk-your-key-here

   Alternatively, create api_key.txt with the same format.
   Both files are git-ignored and will not be shared.

--------------------------------------------------

CONFIGURATION

Edit inputs/week.yaml before each run. Key fields:

  course:
    level          Master or Bachelor
    topics         List of topic strings for this week
    notes_pages    Pages to extract from the PDF, e.g. "23-42"
    target_total_minutes       Total exercise time budget (e.g. 300)
    exercise_class_minutes     Length of the exercise class (default 90)
    policy         Free-text instructions for exercise style

  style_guide:
    template_tex   (optional) A LaTeX preamble/template to mimic

  max_iters        Max pipeline iterations (default 30)

Place your lecture notes at inputs/notes.pdf.
Optionally place a LaTeX template at inputs/template.tex.

--------------------------------------------------

RUNNING

   python -m src.run_week

Outputs appear in out/:

   sheet.tex                Exercise sheet
   solutions.tex            Full solutions
   hints.tex                Hints sheet
   exercise_class_guide.tex Teaching guide
   state.yaml               Full pipeline state (for debugging)

--------------------------------------------------

NOTES

- The LLM model can be changed in src/config.py (DEFAULT_MODEL).
- Each user must provide their own OpenAI API key.
- Do not commit .env or api_key.txt to version control.
