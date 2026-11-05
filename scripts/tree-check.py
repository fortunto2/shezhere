# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Проверка tree.yaml после каждой правки агента: дубли id, битые ссылки, дыры «?».

    uv run scripts/tree-check.py --tree tree.yaml
Выход 0 — структура цела, 1 — ошибки (печатаются по одной на строку).
"""
import argparse
import sys
from collections import Counter
from pathlib import Path

import yaml

REFS = ("father", "mother", "spouse")


def check(people):
    errors = [f"дубль id: {i}" for i, n in Counter(p.get("id") for p in people).items() if n > 1]
    ids = {p.get("id") for p in people}
    for p in people:
        if not p.get("id") or not p.get("name"):
            errors.append(f"нет id или name: {p}")
        for k in REFS:
            v = p.get(k)
            for ref in v if isinstance(v, list) else [v]:
                if ref and ref not in ids:
                    errors.append(f"{p.get('id')}.{k} → {ref}: такого id нет")
        if p.get("father") and p.get("father") == p.get("id"):
            errors.append(f"{p['id']}: сам себе отец")
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", type=Path, default=Path("tree.yaml"))
    a = ap.parse_args()
    people = yaml.safe_load(a.tree.read_text())["people"]
    errors = check(people)
    holes = sum(str(p.get(k, "")).strip() in ("", "?") for p in people for k in ("born",))
    for e in errors:
        print(e)
    print(f"людей {len(people)}, ошибок {len(errors)}, без года рождения {holes}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
