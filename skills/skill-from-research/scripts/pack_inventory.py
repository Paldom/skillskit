#!/usr/bin/env python3
"""Inventory a research pack before anyone reads it.

Usage: pack_inventory.py <path> [<path> ...]
Walks the given files/directories and reports every file with size, type, and
word count; flags EMPTY files, DUPLICATE content (same hash under different
names - it happens), binary/unreadable formats, symlinks that escape the pack,
and per-file read errors. Exit 1 when the pack contains no readable content
(so a pasted-but-empty report fails loudly, before hours of work). Reads are
capped at 8 MB per file (larger files are sampled and flagged). Stdlib only.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

TEXT_EXT = {".md", ".txt", ".rst", ".json", ".jsonl", ".yaml", ".yml", ".csv",
            ".html", ".htm", ".xml", ".log", ".adoc", ""}
SKIP_NAMES = {".DS_Store", "Thumbs.db"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
READ_CAP = 8 * 1024 * 1024  # bytes


def classify(p: Path) -> str:
    if p.suffix.lower() in {".pdf", ".docx", ".pptx", ".xlsx"}:
        return "document (needs extraction)"
    if p.suffix.lower() in TEXT_EXT:
        return "text"
    return "binary/other"


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("ERROR: pass at least one pack path", file=sys.stderr)
        return 1
    files: list[tuple[Path, Path]] = []  # (file, pack_root)
    for a in args:
        p = Path(a)
        if p.is_dir():
            root = p.resolve()
            for f in sorted(p.rglob("*")):
                if any(part in SKIP_DIRS for part in f.parts):
                    continue
                if f.is_file() and f.name not in SKIP_NAMES:
                    files.append((f, root))
        elif p.is_file():
            files.append((p, p.resolve().parent))
        else:
            print(f"WARN: {p} does not exist")
    if not files:
        print("ERROR: the pack contains no files at all")
        return 1

    readable_words = 0
    hashes: dict[str, Path] = {}
    empties, dups, unreadable, escapes, errors, oversized = [], [], [], [], [], []
    print(f"{'size':>9}  {'words':>7}  {'type':<26} file")
    for f, root in files:
        try:
            if f.is_symlink() and not f.resolve().is_relative_to(root):
                escapes.append(f)
                print(f"{'?':>9}  {0:>7}  {'symlink (escapes pack)':<26} {f}")
                continue
            size = f.stat().st_size
        except OSError as exc:
            errors.append((f, exc))
            print(f"{'?':>9}  {0:>7}  {'stat error':<26} {f}")
            continue
        kind = classify(f)
        words = 0
        if size == 0:
            empties.append(f)
        elif kind == "text":
            try:
                raw = f.open("rb").read(READ_CAP + 1)
            except OSError as exc:
                errors.append((f, exc))
                print(f"{size:>9}  {0:>7}  {'read error':<26} {f}")
                continue
            if b"\x00" in raw[:8192]:  # extensionless/mislabeled binaries
                kind = "binary/other"
                unreadable.append(f)
            else:
                if len(raw) > READ_CAP:
                    oversized.append(f)
                    raw = raw[:READ_CAP]
                text = raw.decode("utf-8", errors="replace")
                words = len(text.split())
                readable_words += words
                digest = hashlib.sha256(raw).hexdigest()
                if digest in hashes and words > 0:
                    dups.append((f, hashes[digest]))
                else:
                    hashes[digest] = f
        else:
            unreadable.append(f)
        print(f"{size:>9}  {words:>7}  {kind:<26} {f}")

    print()
    for f in empties:
        print(f"EMPTY: {f} is 0 bytes - if you meant to paste content here, it did not land")
    for f, orig in dups:
        print(f"DUPLICATE: {f} has identical content to {orig}")
    for f in unreadable:
        print(f"UNREADABLE: {f} ({classify(f)}) - extract to text first or it will be skipped")
    for f in escapes:
        print(f"SYMLINK-ESCAPE: {f} points outside the pack - not followed")
    for f, exc in errors:
        print(f"READ-ERROR: {f}: {exc}")
    for f in oversized:
        print(f"OVERSIZED: {f} exceeds the 8 MB cap - inventoried from a sample; read it in chunks")

    print(f"\nTOTAL: {len(files)} file(s), ~{readable_words} readable words"
          f" ({len(empties)} empty, {len(dups)} duplicate, {len(unreadable)} unreadable,"
          f" {len(escapes)} escaping symlink(s), {len(errors)} error(s))")
    if readable_words == 0:
        print("ERROR: no readable content in the pack - nothing to distill")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
