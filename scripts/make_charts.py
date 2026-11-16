#!/usr/bin/env python3
"""Draw a Gantt chart and/or a network diagram from the task table of a schedule document.

Usage:
  python make_charts.py <schedule.md> --gantt gantt.png --network network.png

The markdown file must contain a table with the columns: ID, Task, Start, End, Depends On
(Owner is optional). Dates are best written YYYY-MM-DD. "Depends On" lists task IDs
separated by commas, or is left empty. The network diagram highlights the critical path
(the longest chain of dependent tasks) in red and prints it.
"""
import argparse
import re
import textwrap
from datetime import timedelta

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from dateutil import parser as dateparser  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402


def read_tasks(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    for i, line in enumerate(lines):
        cells = [c.strip().lower() for c in line.strip().strip("|").split("|")]
        if line.strip().startswith("|") and {"id", "task", "start", "end"} <= set(cells):
            header, tasks = cells, []
            for row in lines[i + 2:]:
                if not row.strip().startswith("|"):
                    break
                vals = [c.strip() for c in row.strip().strip("|").split("|")]
                d = dict(zip(header, vals))
                if not d.get("start") or not d.get("end"):
                    continue
                d["start"] = dateparser.parse(d["start"])
                d["end"] = dateparser.parse(d["end"])
                deps = d.get("depends on", "")
                d["deps"] = [x.strip() for x in re.split(r"[,;]", deps) if x.strip() and x.strip() != "-"]
                tasks.append(d)
            return tasks
    raise SystemExit("No task table with ID, Task, Start, End columns found.")


def gantt(tasks, out):
    n = len(tasks)
    fig, ax = plt.subplots(figsize=(10, 0.45 * n + 1.8))
    for k, t in enumerate(tasks):
        y = n - 1 - k
        if t["start"] == t["end"]:
            ax.plot(t["start"], y, marker="D", color="#6c3483", markersize=8)
        else:
            ax.barh(y, (t["end"] - t["start"]).days + 1, left=t["start"], height=0.55,
                    color="#2e6da4")
    ax.set_yticks(range(n))
    ax.set_yticklabels([f"{t['id']}  {t['task'][:38]}" for t in reversed(tasks)], fontsize=8)
    ax.xaxis_date()
    first = min(t["start"] for t in tasks)
    last = max(t["end"] for t in tasks)
    pad = max((last - first).days // 30, 1)
    ax.set_xlim(first - timedelta(days=pad), last + timedelta(days=pad + 1))
    ax.tick_params(axis="x", labelsize=8)
    fig.autofmt_xdate()
    ax.grid(axis="x", alpha=0.3)
    ax.set_title("Project Gantt chart", fontsize=11)
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Gantt chart saved: {out}")


def network(tasks, out):
    by_id = {t["id"]: t for t in tasks}
    dur = {t["id"]: (t["end"] - t["start"]).days + 1 for t in tasks}

    memo = {}

    def finish(i):  # longest path length ending at task i
        if i not in memo:
            preds = [p for p in by_id[i]["deps"] if p in by_id]
            best = max(preds, key=finish, default=None)
            memo[i] = (dur[i] + (finish(best) if best else 0), best)
        return memo[i][0]

    for i in by_id:
        finish(i)
    end_id = max(by_id, key=lambda i: memo[i][0])
    critical, cur = [], end_id
    while cur:
        critical.append(cur)
        cur = memo[cur][1]
    critical.reverse()
    crit_edges = set(zip(critical, critical[1:]))

    level = {}

    def lvl(i):
        if i not in level:
            preds = [p for p in by_id[i]["deps"] if p in by_id]
            level[i] = 1 + max((lvl(p) for p in preds), default=-1)
        return level[i]

    for i in by_id:
        lvl(i)
    cols = {}
    for t in tasks:
        cols.setdefault(level[t["id"]], []).append(t["id"])
    # Long dependency chains make one column per level far too wide for a page,
    # so start a new row of columns after max_cols levels.
    max_cols = 4
    groups = {}
    for c in cols:
        groups.setdefault(c // max_cols, []).append(c)
    group_offset, total_rows = {}, 0
    for group in sorted(groups):
        group_offset[group] = total_rows
        total_rows += max(len(cols[c]) for c in groups[group])

    pos = {}
    for c, ids in cols.items():
        group, col = divmod(c, max_cols)
        for r, i in enumerate(ids):
            pos[i] = (col * 2.05, -(group_offset[group] + r) * 1.55)

    w, h = 1.9, 1.15
    n_cols = min(max_cols, max(cols) + 1)
    fig, ax = plt.subplots(figsize=(2.05 * (n_cols - 1) + w + 0.9, 1.55 * total_rows + 1.3))
    for i, t in by_id.items():
        for p in t["deps"]:
            if p in pos:
                x1, y1 = pos[p]
                x2, y2 = pos[i]
                color = "#c0392b" if (p, i) in crit_edges else "#555555"
                ax.annotate("", xy=(x2, y2), xytext=(x1 + w, y1),
                            arrowprops=dict(arrowstyle="->", color=color,
                                            lw=2 if color == "#c0392b" else 1))
    for i, t in by_id.items():
        x, y = pos[i]
        edge = "#c0392b" if i in critical else "#2e6da4"
        ax.add_patch(FancyBboxPatch((x, y - h / 2), w, h, boxstyle="round,pad=0.02",
                                    fc="white", ec=edge, lw=2 if i in critical else 1))
        ax.text(x + w / 2, y + 0.42, textwrap.fill(f"{i}: {t['task']}", 24),
                ha="center", va="top", fontsize=8, weight="bold", linespacing=1.15)
        ax.text(x + w / 2, y - 0.2, f"{t['start']:%m-%d} to {t['end']:%m-%d}",
                ha="center", va="center", fontsize=7.5)
        ax.text(x + w / 2, y - 0.42, f"{dur[i]} days", ha="center", va="center", fontsize=7.5)
    ax.set_xlim(-0.25, 2.05 * (n_cols - 1) + w + 0.25)
    ys = [p[1] for p in pos.values()]
    ax.set_ylim(min(ys) - 0.8, max(ys) + 0.8)
    ax.axis("off")
    ax.set_title("Network diagram (critical path in red)", fontsize=10)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.02)
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Network diagram saved: {out}")
    print("Critical path: " + " -> ".join(critical)
          + f"  ({memo[end_id][0]} days)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("schedule_md")
    ap.add_argument("--gantt")
    ap.add_argument("--network")
    a = ap.parse_args()
    tasks = read_tasks(a.schedule_md)
    if a.gantt:
        gantt(tasks, a.gantt)
    if a.network:
        network(tasks, a.network)
