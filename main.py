#!/usr/bin/env python3
"""Real-Life Patch Notes: The Comedy Changelog — make.fun entry.

Writes one line, a software patch note for a bug in real life / human
biology, to /output/entry.txt. Pure Python standard library, fully
deterministic: the same bytes on every run.
"""

import os
import sys

# The entry: a terse release note for a bug every human ships with —
# the brain replaying an old embarrassment at 3 a.m. Version number,
# dry engineering register, one specific recognisable bug, punchline
# that lands on first read ("in full surround sound").
ENTRY = (
    "v2.7.1: fixed a bug where the brain replayed your most "
    "embarrassing moment from 2009 at 3:00 a.m. in full surround sound."
)

MAX_CHARS = 160


def validate(text):
    """Enforce the competition gate: 1-160 chars, not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise ValueError(
            "entry must be 1 to %d characters, got %d" % (MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line (no newline)")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry must not contain control characters")
    return text


def main():
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Read back what landed on disk and re-validate it.
    with open(path, "rb") as f:
        raw = f.read()
    landed = raw.decode("utf-8")
    validate(landed)
    if landed != ENTRY:
        raise ValueError("entry on disk differs from ENTRY")
    # Genuine check added this session: the byte count on disk must
    # match the entry exactly (guards against a stray newline or BOM).
    expected_bytes = len(ENTRY.encode("utf-8"))
    if len(raw) != expected_bytes:
        raise ValueError(
            "entry on disk is %d bytes, expected %d" % (len(raw), expected_bytes)
        )
    print("entry (%d chars): %s" % (len(landed), landed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
