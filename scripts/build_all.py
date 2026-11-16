#!/usr/bin/env python3
"""Rebuild every document in a project's docs folder, and keep the index up to date.

Usage: python build_all.py <docs_dir> [--force]

Layout:
    <docs_dir>/source/<phase folder>/<name>.md   source of truth (Claude edits these)
    <docs_dir>/<phase folder>/<name>.docx        built Word files

Only documents whose .md changed are rebuilt. If a .docx was edited by hand
(by the user, in Word), it is NOT overwritten: a warning is printed so the
changes can be copied into the .md first. --force rebuilds everything anyway.
"""
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_doc import build, parse_front_matter  # noqa: E402

INDEX_NAME = "00_Document_Index.md"


def sha(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def read_meta(path):
    with open(path, encoding="utf-8") as f:
        meta, _ = parse_front_matter(f.read().splitlines())
    return meta


def find_sources(source_dir):
    found = []
    for root, _dirs, files in os.walk(source_dir):
        for name in files:
            if name.endswith(".md"):
                found.append(os.path.relpath(os.path.join(root, name), source_dir))
    return sorted(found)


def phase_of(rel):
    folder = os.path.dirname(rel)
    return re.sub(r"^\d+_", "", folder).replace("_", " ") if folder else "General"


def write_index(source_dir, rels):
    rows, project, author, dates = [], "", "", []
    for rel in rels:
        if rel == INDEX_NAME:
            continue
        meta = read_meta(os.path.join(source_dir, rel))
        project = project or meta.get("project", "")
        author = author or meta.get("author", "")
        dates.append(meta.get("date", ""))
        rows.append(f"| {len(rows) + 1} | {meta.get('title', rel)} | {phase_of(rel)} | "
                    f"{meta.get('version', '')} | {meta.get('date', '')} | "
                    f"{meta.get('status', 'Final')} |")
    text = (f"---\ntitle: Document Index\nproject: {project}\nauthor: {author}\n"
            f"version: -\ndate: {max(dates) if dates else ''}\n---\n"
            "# Documents\n"
            "This index lists every document of the project, its phase, and its current version.\n\n"
            "| No. | Document | Phase | Version | Date | Status |\n|---|---|---|---|---|---|\n"
            + "\n".join(rows) + "\n")
    path = os.path.join(source_dir, INDEX_NAME)
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    if old != text:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    if len(args) != 1:
        sys.exit("Usage: python build_all.py <docs_dir> [--force]")
    docs_dir = os.path.abspath(args[0])
    source_dir = os.path.join(docs_dir, "source")
    state_path = os.path.join(docs_dir, ".build_state.json")
    state = json.load(open(state_path)) if os.path.exists(state_path) else {}

    rels = find_sources(source_dir)
    write_index(source_dir, rels)
    rels = find_sources(source_dir)  # the index may be new

    built = skipped = 0
    for rel in rels:
        md = os.path.join(source_dir, rel)
        out = os.path.join(docs_dir, rel[:-3] + ".docx")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        md_sha = sha(md)
        old = state.get(rel, {})
        hand_edited = os.path.exists(out) and old and sha(out) != old.get("docx")
        needs_build = (not os.path.exists(out)) or md_sha != old.get("md") or force

        if hand_edited and not force:
            print(f"WARNING: {os.path.relpath(out, docs_dir)} was edited by hand. "
                  f"Copy those changes into source/{rel} first, then rebuild with --force.")
            skipped += 1
        elif needs_build:
            build(md, out)
            state[rel] = {"md": md_sha, "docx": sha(out)}
            built += 1
        else:
            skipped += 1

    with open(state_path, "w") as f:
        json.dump(state, f, indent=1)
    print(f"Done: {built} built, {skipped} unchanged or skipped.")


if __name__ == "__main__":
    main()
