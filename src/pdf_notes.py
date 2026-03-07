from pypdf import PdfReader


def parse_page_spec(page_spec):
    """
    Accepts either:
    - a list of ints, e.g. [35, 36, 37, 38]
    - a string, e.g. "35-38" or "35-38,41,43-45"

    Returns a sorted list of unique page numbers.
    """
    if page_spec is None:
        return []

    if isinstance(page_spec, list):
        pages = []
        for p in page_spec:
            if not isinstance(p, int):
                raise ValueError(f"Invalid page entry {p!r}; expected integers.")
            pages.append(p)
        return sorted(set(pages))

    if isinstance(page_spec, str):
        pages = set()
        parts = [part.strip() for part in page_spec.split(",") if part.strip()]

        for part in parts:
            if "-" in part:
                a, b = part.split("-", 1)
                try:
                    start = int(a.strip())
                    end = int(b.strip())
                except ValueError:
                    raise ValueError(f"Invalid page range {part!r}. Expected format like '35-38'.")

                if start > end:
                    raise ValueError(f"Invalid page range {part!r}: start must be <= end.")

                for p in range(start, end + 1):
                    pages.add(p)
            else:
                try:
                    pages.add(int(part))
                except ValueError:
                    raise ValueError(f"Invalid page entry {part!r}. Expected an integer or range like '35-38'.")

        return sorted(pages)

    raise ValueError(
        f"Unsupported notes_pages format: {type(page_spec).__name__}. "
        "Use either a list like [35, 36, 37] or a string like '35-38,41'."
    )


def extract_notes(pdf_path, page_spec):
    reader = PdfReader(pdf_path)
    n_pages = len(reader.pages)

    pages = parse_page_spec(page_spec)
    if not pages:
        return ""

    bad_pages = [p for p in pages if p < 1 or p > n_pages]
    if bad_pages:
        raise ValueError(
            f"Invalid notes_pages {bad_pages}. "
            f"The PDF '{pdf_path}' has {n_pages} pages, so valid pages are 1 to {n_pages}."
        )

    text = []
    for p in pages:
        page_text = reader.pages[p - 1].extract_text() or ""
        text.append(f"\n--- PAGE {p} ---\n{page_text}")

    return "\n\n".join(text)