#!/usr/bin/env python3
"""NPV, ROI and payback table for the Business Case (textbook method, Ch. 4).

Usage:
  python finance.py --rate 0.08 --costs 140000,40000,40000,40000 \
                    --benefits 0,200000,200000,200000 [--round-factors] [--chart payback.png]

Each number in --costs / --benefits is one year, starting with Year 0 (the
development year). Year 0 is not discounted, as in the textbook example.
--round-factors rounds discount factors to 2 decimals like the textbook figures.
Prints markdown that can be pasted into the Business Case.
"""
import argparse


def money(x):
    r = round(x)
    return f"({abs(r):,})" if r < 0 else f"{r:,}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rate", type=float, required=True, help="discount rate, e.g. 0.08")
    ap.add_argument("--costs", required=True)
    ap.add_argument("--benefits", required=True)
    ap.add_argument("--round-factors", action="store_true")
    ap.add_argument("--currency", default="$", help="currency symbol used in the text output")
    ap.add_argument("--chart", help="optional PNG path for the payback chart")
    a = ap.parse_args()

    costs = [float(x) for x in a.costs.split(",")]
    benefits = [float(x) for x in a.benefits.split(",")]
    if len(costs) != len(benefits):
        raise SystemExit("--costs and --benefits need the same number of years")
    n = len(costs)

    factors = [1 / (1 + a.rate) ** t for t in range(n)]
    if a.round_factors:
        factors = [round(f, 2) for f in factors]
    dc = [c * f for c, f in zip(costs, factors)]
    db = [b * f for b, f in zip(benefits, factors)]
    net = [b - c for b, c in zip(db, dc)]
    cum, run = [], 0.0
    for v in net:
        run += v
        cum.append(run)

    npv = sum(net)
    roi = npv / sum(dc)
    payback = next((t for t, v in enumerate(cum) if v >= 0), None)

    head = "| Item | " + " | ".join(f"Year {t}" for t in range(n)) + " | Total |"
    sep = "|---|" + "---|" * (n + 1)

    def row(label, vals, total=None):
        t = "" if total is None else money(total)
        return f"| {label} | " + " | ".join(money(v) for v in vals) + f" | {t} |"

    print(f"Discount rate: {a.rate:.0%}\n")
    print(head)
    print(sep)
    print(row("Costs", costs, sum(costs)))
    print("| Discount factor | " + " | ".join(f"{f:.2f}" for f in factors) + " | |")
    print(row("Discounted costs", dc, sum(dc)))
    print(row("Benefits", benefits, sum(benefits)))
    print(row("Discounted benefits", db, sum(db)))
    print(row("Discounted benefits minus costs", net, npv))
    print(row("Cumulative benefits minus costs", cum))
    print()
    print(f"- Net present value (NPV): {a.currency}{money(npv)}")
    print(f"- Return on investment (ROI): {roi:.0%}")
    print("- Payback: " + (f"Year {payback}" if payback is not None
                           else f"not reached within {n - 1} years"))

    if a.chart:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        cc, cb, s1, s2 = [], [], 0, 0
        for c, b in zip(dc, db):
            s1 += c
            s2 += b
            cc.append(s1)
            cb.append(s2)
        fig, ax = plt.subplots(figsize=(7, 3.6))
        ax.plot(range(n), cc, marker="o", color="#b03a2e", label="Cumulative costs")
        ax.plot(range(n), cb, marker="o", color="#1f6f43", label="Cumulative benefits")
        ax.set_xticks(range(n))
        ax.set_xticklabels([f"Year {t}" for t in range(n)])
        ax.set_ylabel("Value (discounted)")
        ax.yaxis.set_major_formatter(lambda v, _: f"{v:,.0f}")
        ax.grid(alpha=0.3)
        ax.legend()
        ax.set_title("Payback chart")
        fig.tight_layout()
        fig.savefig(a.chart, dpi=200)
        print(f"\nChart saved: {a.chart}")


if __name__ == "__main__":
    main()
