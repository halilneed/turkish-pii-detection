"""Evaluate supplied outputs; no inference, training, or network access.

Smoke fixtures are deliberately handwritten. They are not model predictions.
Python 3.9+; standard library only.
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path


def load_rows(path):
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    ids = [r.get("id") for r in rows]
    if not rows or any(not isinstance(i, str) or not i for i in ids) or len(ids) != len(set(ids)):
        raise ValueError("Rows must be nonempty and have unique, nonempty string IDs")
    return {r["id"]: r for r in rows}


def evaluate(cases, predictions):
    if set(cases) != set(predictions):
        raise ValueError("Case/prediction IDs must match exactly; missing outputs cannot be dropped")
    groups = defaultdict(list)
    for key, case in cases.items():
        output = predictions[key].get("output")
        if not isinstance(output, str):
            raise ValueError("Prediction output must be a string")
        if not isinstance(case.get("expected"), str) or not isinstance(case.get("slice"), str) or not case["slice"]:
            raise ValueError("Case expected and nonempty slice strings are required")
        for field in ("must_remove", "must_keep"):
            if field not in case or not isinstance(case[field], list) or any(not isinstance(v, str) or not v for v in case[field]):
                raise ValueError("must_remove/must_keep must be lists of nonempty literal strings")
        result = {
            "id": key,
            "exact_match": output == case["expected"],
            "remove_checks": len(case["must_remove"]),
            "literal_leaks": sum(v in output for v in case["must_remove"]),
            "keep_checks": len(case["must_keep"]),
            "missing_kept_literals": sum(v not in output for v in case["must_keep"]),
        }
        groups[case["slice"]].append(result)

    def summarize(rows):
        n = len(rows)
        remove_n = sum(r["remove_checks"] for r in rows)
        keep_n = sum(r["keep_checks"] for r in rows)
        return {
            "n": n,
            "exact_match_rate": sum(r["exact_match"] for r in rows) / n if n else None,
            "literal_remove_checks": remove_n,
            "literal_leak_rate": sum(r["literal_leaks"] for r in rows) / remove_n if remove_n else None,
            "literal_keep_checks": keep_n,
            "missing_kept_literal_rate": sum(r["missing_kept_literals"] for r in rows) / keep_n if keep_n else None,
        }

    all_rows = [r for rows in groups.values() for r in rows]
    return {"overall": summarize(all_rows), "slices": {s: summarize(v) for s, v in sorted(groups.items())}, "cases": all_rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", required=True)
    parser.add_argument("--predictions", required=True)
    args = parser.parse_args()
    print(json.dumps(evaluate(load_rows(args.cases), load_rows(args.predictions)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
