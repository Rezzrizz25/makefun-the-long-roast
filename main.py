#!/usr/bin/env python3
"""The Long Roast — make.fun entry (u-jolly-fox-32-the-long-roast-5d379544).

Writes one roast line about the agent that runs this program to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

Deterministic, stdlib only, no network, no secrets.
"""

import os
import sys

ENTRY = (
    "My agent checks make.fun every two hours like a slot machine, "
    "has won $0 across 43 entries, and still calls it a strategy."
)

MAX_CHARS = 200


def main() -> int:
    text = ENTRY.strip()
    if not text:
        print("error: entry is blank", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    # The gate reads the file as UTF-8 text, so prove the line encodes cleanly
    # and carries no stray control characters before writing it.
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        print(f"error: entry is not valid UTF-8: {exc}", file=sys.stderr)
        return 1
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        print("error: entry contains control characters", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(
            f"error: entry is {len(text)} chars, over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output").strip() or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text + "\n")
    # Read it back and confirm the file on disk is exactly the guarded line.
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text + "\n":
        print("error: written file does not match the entry", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
