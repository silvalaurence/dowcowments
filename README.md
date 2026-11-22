<img src="site/logo.svg" alt="dowcowments" width="370">

Turn a project folder into the full set of formal project documents — one cleanly formatted Word file per document — and keep them up to date when the project changes. Built for student and small-team projects that have to hand in paperwork: business case, charter, stakeholder register, scope statement, WBS, schedule with Gantt chart, budget, risk register, test plan, progress reports, lessons learned, final report, and the rest.

Markdown is the source of truth. Word files are built from it, never edited by hand. Only changed documents are rebuilt, and the build refuses to overwrite a `.docx` someone edited in Word.

## Run

Python 3.9 or newer.

1. `git clone https://github.com/<you>/dowcowments.git && cd dowcowments`
2. `pip install -r requirements.txt`
3. `python scripts/build_all.py example/docs` — builds the bundled example (a project schedule, a charter, and a document index).
4. For your own project, create `docs/source/<phase>/<name>.md` with a header of `title`, `project`, `author`, `version`, `date`, `status`, then run `python scripts/build_all.py docs`.
5. `python scripts/build_doc.py <input.md> <output.docx>` builds a single document. `make_charts.py` draws Gantt and network diagrams (critical path in red); `finance.py` computes NPV, ROI, and payback.

Headings (`#`, `##`, `###`) become numbered headings automatically — don't type the numbers. Bullets, numbered lists, bold, tables, `![Caption](../assets/chart.png)`, and `<pagebreak>` are supported. Every document gets Arial 12 pt, 1.15 line spacing, 1 inch margins, a version/date/author/status table, and page numbers.

`SKILL.md` makes the workflow available to an AI coding agent; copy this folder into your agent's skills directory (for Qoder, `~/.qoder/skills/docowment`). The scripts also run on their own with no agent involved.

## Files

- `SKILL.md` — agent instructions: what to write, what to update, writing rules
- `references/doc-outlines.md` — 40 documents across five process groups, plus 5 Scrum documents and extras
- `scripts/` — build, single-document, chart, and finance helpers
- `example/docs/source/` — a small working example
- `site/logo.svg` — README logo

No license file yet — add one before publishing if you want others to reuse it.
