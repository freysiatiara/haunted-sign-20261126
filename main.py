"""Write the haunted server room door sign to the entry file.

Stdlib only. The output path resolves from ENTRY_OUTPUT, then from
OUTPUT_DIR / MAKEFUN_OUTPUT_DIR (joined with "entry.txt"), then the
default /output/entry.txt -- never the current working directory.
The text is written with a plain open/write and chmodded 0644, so the
grader sees a normal readable file.
"""

import os

LINE = "DO NOT KNOCK. THE GHOST IN THERE ALREADY KNOWS YOUR PASSWORD. HE CHANGED IT."


def resolve_output_path() -> str:
    explicit = os.environ.get("ENTRY_OUTPUT")
    if explicit:
        return explicit
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        directory = os.environ.get(var)
        if directory:
            return os.path.join(directory, "entry.txt")
    return "/output/entry.txt"


def main() -> None:
    text = LINE
    # Validation guard: the gate wants 1..120 UTF-8 chars, not only whitespace.
    assert text.strip(), "entry text must not be blank"
    assert 1 <= len(text) <= 120, "entry text must be 1..120 characters"
    encoded = text.encode("utf-8")
    assert len(encoded) == len(text), "entry text must be plain ASCII"
    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    # Round-trip check: what landed on disk must be exactly the line.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        assert handle.read() == text, "written entry differs from the line"


if __name__ == "__main__":
    main()
