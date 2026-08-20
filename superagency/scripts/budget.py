#!/usr/bin/env python3
"""Budget arithmetic: back-solve to a goal, split a portfolio, check payback.

budget.md says to start from the goal and work backwards, and to say so when
the math doesn't reach it rather than distributing the shortfall quietly.
That's a four-step chain where a slipped decimal is invisible.

  python3 scripts/budget.py backsolve --target 3000 --conv-rate 0.02 --cpc 2.40 --budget 100000
  python3 scripts/budget.py split --total 40000
  python3 scripts/budget.py payback --cac 300 --arpu 50 --margin 0.8
"""
import argparse
import json
import sys


def backsolve(target, conv_rate, cpc, budget=None):
    if not 0 < conv_rate <= 1:
        raise ValueError("--conv-rate must be between 0 and 1")
    if cpc <= 0 or target <= 0:
        raise ValueError("--cpc and --target must be positive")
    visits = target / conv_rate
    spend = visits * cpc
    out = {"target_conversions": target, "conversion_rate": conv_rate,
           "visits_required": round(visits), "cpc": cpc,
           "spend_required": round(spend, 2), "cost_per_conversion": round(cpc / conv_rate, 2)}
    if budget is not None:
        out["budget_given"] = budget
        out["reaches_goal"] = budget >= spend
        if budget < spend:
            out["shortfall"] = round(spend - budget, 2)
            out["conversions_affordable"] = round((budget / cpc) * conv_rate)
    return out


def split(total, weights):
    labels = ("proven", "scaling", "experiment")
    if abs(sum(weights) - 1.0) > 1e-9:
        raise ValueError(f"weights must sum to 1.0, got {sum(weights)}")
    return {"total": total,
            "allocation": {l: round(total * w, 2) for l, w in zip(labels, weights)},
            "weights": dict(zip(labels, weights))}


def payback(cac, arpu, margin):
    if arpu <= 0 or not 0 < margin <= 1:
        raise ValueError("--arpu must be positive and --margin between 0 and 1")
    monthly = arpu * margin
    return {"cac": cac, "arpu": arpu, "gross_margin": margin,
            "monthly_contribution": round(monthly, 2),
            "payback_months": round(cac / monthly, 1)}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("backsolve", help="goal -> traffic -> spend")
    b.add_argument("--target", type=float, required=True, help="target conversions")
    b.add_argument("--conv-rate", type=float, required=True, help="e.g. 0.02")
    b.add_argument("--cpc", type=float, required=True, help="cost per visit")
    b.add_argument("--budget", type=float, help="budget on hand, to test against the goal")

    s = sub.add_parser("split", help="portfolio allocation")
    s.add_argument("--total", type=float, required=True)
    s.add_argument("--proven", type=float, default=0.70)
    s.add_argument("--scaling", type=float, default=0.20)
    s.add_argument("--experiment", type=float, default=0.10)

    y = sub.add_parser("payback", help="months to recover CAC")
    y.add_argument("--cac", type=float, required=True)
    y.add_argument("--arpu", type=float, required=True, help="monthly revenue per user")
    y.add_argument("--margin", type=float, default=0.80, help="gross margin, e.g. 0.8")

    args = p.parse_args(argv)
    try:
        if args.cmd == "backsolve":
            out = backsolve(args.target, args.conv_rate, args.cpc, args.budget)
        elif args.cmd == "split":
            out = split(args.total, (args.proven, args.scaling, args.experiment))
        else:
            out = payback(args.cac, args.arpu, args.margin)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(out, indent=2))
    elif args.cmd == "backsolve":
        print(f"{out['target_conversions']:,.0f} conversions at {out['conversion_rate']:.2%} "
              f"needs {out['visits_required']:,} visits")
        print(f"At ${out['cpc']:.2f}/visit: ${out['spend_required']:,.2f} "
              f"(${out['cost_per_conversion']:,.2f} per conversion)")
        if "reaches_goal" in out:
            if out["reaches_goal"]:
                print(f"Budget of ${out['budget_given']:,.2f} covers it.")
            else:
                print(f"\nBudget of ${out['budget_given']:,.2f} does NOT reach the goal.")
                print(f"  Short by ${out['shortfall']:,.2f}; it buys "
                      f"{out['conversions_affordable']:,} conversions, not {out['target_conversions']:,.0f}.")
                print("  Say this plainly rather than spreading the shortfall across channels.")
    elif args.cmd == "split":
        for label, amount in out["allocation"].items():
            print(f"{label:11} ${amount:>12,.2f}  ({out['weights'][label]:.0%})")
    else:
        print(f"Monthly contribution: ${out['monthly_contribution']:,.2f}")
        print(f"Payback: {out['payback_months']} months")
    return 0


if __name__ == "__main__":
    sys.exit(main())
