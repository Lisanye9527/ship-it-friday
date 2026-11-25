"""Entry for make.fun bounty "Ship It Friday".

Writes one line of text -- the funniest git commit message an AI coding
agent writes in the moment before it breaks production on a Friday --
to ``$MAKEFUN_OUTPUT_DIR/entry.txt`` (``/output`` when the variable is
unset, matching the grader container).

The line is a constant, so the program is deterministic: every run
writes exactly the same bytes. Before writing, the program checks the
line against the bounty gate (UTF-8 text of 1 to 159 characters, not
only white space, a single line) and fails loudly if it ever drifts
out of bounds.

Run it from the repository root, for example:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import sys
from pathlib import Path

COMMIT_MESSAGE = (
    "fix: reviewed my own pull request and approved it in record time. "
    "deploying to production friday 4:59 pm, then logging off. "
    "happy weekend, everyone!"
)

MAX_CHARS = 159


def main() -> int:
    line = COMMIT_MESSAGE
    if not line.strip():
        print("error: the commit message is empty", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("error: the commit message must be a single line", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            f"error: the commit message is {len(line)} characters, over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip() or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.txt"
    dest.write_text(line, encoding="utf-8")
    written = dest.read_text(encoding="utf-8")
    if written != line:
        print("error: written text differs from the commit message", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({len(line)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
