<p align="center">
  <img src="dowcowments-logo.svg" width="560" alt="dowcowments">
</p>

> Move your documents in project manager.

Turn a project folder into the full set of formal project documents — one cleanly formatted Word file per document — and keep them up to date when the project changes.

Built for student and small-team projects that have to hand in paperwork: business case, charter, stakeholder register, scope statement, WBS, schedule with Gantt chart, budget, risk register, test plan, progress reports, lessons learned, final report, and the rest.

## How it works

Markdown is the source of truth. Word files are built from it, never edited by hand.

```
your-project/docs/
    00_Document_Index.docx        generated list of every document
    1_Initiating/  2_Planning/  3_Executing/
    4_Monitoring_Controlling/  5_Closing/  Scrum/
        *.docx                    built output, ready to hand in
    source/                       same folders, one .md per document
        assets/                   charts and pictures
```

Only changed documents are rebuilt. If someone edits a `.docx` in Word, the build refuses to overwrite it and prints a warning, so their edits are never lost.

Every document gets the same layout: Arial 12 pt, 1.15 line spacing, 1 inch margins, numbered bold headings, a version/date/author/status table on top, and page numbers in the footer.

## What's in the set

`references/doc-outlines.md` defines 40 documents across the five process groups, plus 5 Scrum documents and optional extras. Each entry lists the exact sections and table columns, so documents stay consistent with each other.

| Folder | Documents |
|---|---|
| 1_Initiating | 7 — business case, project selection, statement of work, charter, stakeholder register and strategy, kickoff |
| 2_Planning | 17 — management plan, requirements, traceability, scope, WBS, schedule, cost, quality, HR, communications, risk, procurement, change control, test plan |
| 3_Executing | 4 — milestone report, technical design, test report, benefits measurement |
| 4_Monitoring_Controlling | 6 — progress report, change request, issue log, expectations matrix, earned value, phase exit review |
| 5_Closing | 6 — lessons learned, client acceptance, final report, contract closeout, post-implementation review, presentation outline |
| Scrum | 5 — vision, backlog, release plan, sprint plan, review and retrospective |

## Install

Python 3.9 or newer.

```bash
git clone https://github.com/<you>/docowment.git
cd docowment
pip install -r requirements.txt
```

## Quickstart

Build the bundled example:

```bash
python scripts/build_all.py example/docs
```

That writes `example/docs/2_Planning/08_Project_Schedule.docx`, `example/docs/1_Initiating/04_Project_Charter.docx`, and a document index.

For your own project, create `docs/source/<phase>/<name>.md` with a header like this, then build:

```markdown
---
title: Project Charter
project: Library Management System
author: Team Example
version: 1.0
date: 2026-11-16
status: Final
---
# Introduction
Plain paragraph text.

| Name | Role |
|---|---|
| Ana | Project Manager |

# Revision History
| Version | Date | Description | Author |
|---|---|---|---|
| 1.0 | 2026-11-16 | First draft | Team Example |
```

`#`, `##`, `###` become numbered headings automatically — don't type the numbers. Also supported: `-` bullets, `1.` numbered lists, `**bold**`, tables, `![Caption](../assets/chart.png)`, and `<pagebreak>`.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/build_all.py <docs_dir> [--force]` | Rebuild changed documents and refresh the index |
| `scripts/build_doc.py <input.md> <output.docx>` | Build a single document |
| `scripts/make_charts.py <schedule.md> --gantt g.png --network n.png` | Gantt chart and network diagram with the critical path in red |
| `scripts/finance.py --rate 0.08 --costs ... --benefits ... [--chart payback.png]` | NPV, ROI and payback table for the business case |

The schedule table needs `ID, Task, Start, End, Depends On` columns with `YYYY-MM-DD` dates. `finance.py` takes one number per year starting at Year 0, which is not discounted.

```bash
python scripts/make_charts.py example/docs/source/2_Planning/08_Project_Schedule.md \
  --gantt example/docs/source/assets/gantt.png \
  --network example/docs/source/assets/network.png

python scripts/finance.py --rate 0.08 --costs 140000,40000,40000,40000 \
  --benefits 0,200000,200000,200000 --chart payback.png
```

## Use it as an agent skill

`SKILL.md` makes the whole workflow available to an AI coding agent: it reads your project, writes the markdown sources, runs the helpers, and updates the right documents when you say "we added a login feature" or "the deadline moved".

Copy this folder into your agent's skills directory (for Qoder, `~/.qoder/skills/docowment`) and it is picked up as the `docowment` skill. The scripts also work on their own with no agent involved.

## Layout

```
SKILL.md                  agent instructions: what to write, what to update, writing rules
references/doc-outlines.md  every document, its sections and table columns
scripts/                  the four build and chart scripts
example/docs/source/      a small working example
```

## License

No license file yet — add one before publishing if you want others to reuse it.