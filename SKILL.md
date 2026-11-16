---
name: docowment
description: Create and update the complete set of formal school/IT project documents (business case, charter, stakeholder register, scope statement, WBS, schedule with Gantt chart, budget, risk register, communications plan, test plan, progress and milestone reports, lessons learned, final report, Scrum backlog and sprint documents, and more) as separate, cleanly formatted Word (.docx) files built from the user's project folder. Use this whenever the user asks for project documentation, "documents for our project", a formal paper for a teacher, or says things like "we changed X, update the docs", "add this to the docs", "we finished the sprint", "new teammate", "deadline moved", "we're done", even if they don't name a specific document.
---

# docowment

Move your documents in project manager.

Turns a project folder into the full set of formal project documents (based on Chapters 1 to 4 of the course book, organized by the five process groups), one Word file per document, and keeps them up to date when the project changes. The goal is documents a teacher can read quickly: plain words, short sections, identical layout everywhere.

## Folder layout

Work inside the user's project folder. Create this if it does not exist:

```
<project folder>/docs/
    00_Document_Index.docx        <- built automatically, lists every document
    1_Initiating/   2_Planning/   3_Executing/
    4_Monitoring_Controlling/     5_Closing/     Scrum/    <- the .docx files to hand in
    source/                       <- same folders, with one .md per document (source of truth)
    source/assets/                <- charts and pictures used by the documents
```

The agent edits only the `.md` files. The `.docx` files are rebuilt from them, which keeps updates cheap and the formatting identical. Never edit a `.docx` directly.

## Making the documents

1. **Read the project folder first** (README, notes, code, existing docs, anything dropped in). Pull the project name, team, topic, features, dates, tools, and methodology (Scrum, waterfall, and so on) from what is there. Ask only for what is truly missing, usually project name, team members with roles, and deadline. One short question, not a questionnaire.
2. **Build the whole set** listed in `references/doc-outlines.md`, using each document's sections and table columns. Skip the `Scrum/` folder unless the team uses Scrum or the user mentions sprints. Skip Procurement and Contract Closeout if nothing is bought or outsourced (say so in one line instead).
3. **Fill what is known, mark what is not.** Use the real project details. Where information does not exist yet, write `[To be decided]` rather than inventing it. Documents for phases not reached yet (Executing, Monitoring, Closing) are still created, with `status: Draft - not started yet` in the header, so the teacher sees the full structure and later updates fill them in.
4. **Use the helper scripts** instead of working numbers or pictures out by hand:
   - Business Case money table, NPV, ROI, payback: `python <skill-path>/scripts/finance.py --rate 0.08 --costs 140000,40000,40000,40000 --benefits 0,200000,200000,200000 --chart docs/source/assets/payback.png` (Year 0 first; prints markdown to paste).
   - Gantt chart and network diagram with critical path, drawn from the task table in the schedule document: `python <skill-path>/scripts/make_charts.py docs/source/2_Planning/08_Project_Schedule.md --gantt docs/source/assets/gantt.png --network docs/source/assets/network.png`
   - Insert pictures in a document with `![Figure caption](../assets/gantt.png)` (path relative to the .md file).
5. **Build:** `python <skill-path>/scripts/build_all.py docs`. It rebuilds only changed documents and refreshes the index.
6. **Check** one output by converting it to PDF and looking at it. Then tell the user what was created and which blanks remain, in a few lines.

## Updating documents

When the user says something changed ("we added a login feature", "Maria joined", "deadline is now Dec 5", "sprint 2 is done", "we are finished"):

1. Run `build_all.py` once first. If it prints a WARNING that a `.docx` was edited by hand, read that `.docx`, copy its changes into the matching `.md`, and rebuild with `--force`. The user's edits must never be lost.
2. Decide which documents the change touches (table below), and create any missing recurring document (a new progress report, change request, sprint review, and so on). Edit only those `.md` files.
3. In each changed file: raise `version` (1.0 to 1.1 for a small change, 2.0 for a big one), set `date` to today, update `status` if it changed (Draft, In progress, Final), and add one row to the Revision History table saying what changed.
4. Re-run the helper scripts if the change affects money or the schedule, then run `build_all.py docs`.
5. Reply with one line per file changed. Nothing more.

| What changed | Documents usually affected |
|---|---|
| Feature added, removed, or changed | Scope Statement, Requirements Document, Traceability Matrix, WBS, Schedule, Cost Estimate, Risk Register, Test Plan, Product Backlog, Change Request |
| Deadline or milestone moved | Charter, Schedule, Milestone Report, Release Plan, Communications Plan |
| Team member joined, left, or changed role | Charter, Stakeholder Register, Team Contract, Human Resource Plan, Communications Plan |
| Budget or cost change | Business Case, Charter, Cost Estimate, Earned Value Report, Change Request |
| New problem or risk | Risk Register, Issue Log, Progress Report |
| Something was bought or outsourced | Procurement Plan, Cost Estimate, Risk Register |
| Weekly update | Progress Report (new file), Issue Log |
| Milestone reached | Milestone Report, Schedule, Earned Value Report |
| A phase ended | Phase Exit Review, Milestone Report |
| Test finished | Test Report, Issue Log, Requirements Traceability Matrix |
| Sprint finished | Sprint Review and Retrospective (new file), Product Backlog, Release Plan, Progress Report |
| Project finished | Lessons Learned, Client Acceptance Form, Final Report, Final Presentation Outline, Contract Closeout, Post-Implementation Review |

## Markdown the builder understands

Put this header first, then the body:

```
---
title: Project Charter
project: Library Management System
author: Team Name
version: 1.0
date: 2026-11-07
status: Final
---
# Introduction
Normal paragraph text.
## Purpose
- Bullet item
1. Numbered item

| Name | Role |
|---|---|
| Ana | Project Manager |

![Figure caption](../assets/chart.png)
<pagebreak>
```

`#`, `##`, `###` become numbered headings (1, 1.1, 1.1.1) automatically. Do not type the numbers yourself. End every document with `# Revision History` and a table `| Version | Date | Description | Author |`. Write dates as `YYYY-MM-DD` in the schedule table so the chart script can read them.

## Writing rules

These exist because the reader is a teacher grading many papers, not a specialist.

- Short sentences. Plain words. Say "use" not "utilize".
- One idea per paragraph, three to five sentences at most.
- Prefer a small table over a long paragraph when listing people, dates, risks, or costs.
- Spell out an acronym the first time (Work Breakdown Structure (WBS)).
- Formal tone, no slang, no first person ("we" is fine for the team in the charter and lessons learned).
- Use the real project name everywhere. Never leave template wording like "[Project Name]".
- Make documents agree with each other. The same dates, budget, team names, and feature list must appear everywhere they are mentioned, so check the Charter, Scope Statement, Schedule, and Cost Estimate against each other before building.

## Formatting (handled by the scripts, do not override)

Arial 12 pt, 1.15 line spacing, 1 inch margins, 0.5 inch first-line indent on body paragraphs, left-aligned, bold numbered headings, a small document-info table on top (version, date, author, status), page numbers in the footer. Word measures text in points, so "12" here means 12 pt, the normal Word size.
