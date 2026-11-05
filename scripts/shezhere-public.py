# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Публичная версия одной линии шежере: старые колена с именами, новые — свёрнуты.

    uv run scripts/shezhere-public.py --tree tree.yaml --from <id>              # линия отца, Mermaid
    uv run scripts/shezhere-public.py --tree tree.yaml --from <id> --line mother --list

Правило, а не глаз: человек открыт, если родился раньше BORN_BEFORE или умер больше
DIED_YEARS лет назад (столько же закрыты дела с личной и семейной тайной по 125-ФЗ, ст. 25).
Предок открытого человека тоже открыт: он старше. Все остальные — живые, их дети и те, о ком
ничего не известно, — сворачиваются в один узел без имён. Ниже `--from` (дети) не выводится.
"""
import argparse
import re
import sys
import time
from pathlib import Path

import yaml

BORN_BEFORE = 1900
DIED_YEARS = 75


def year(v):
    """Первый четырёхзначный год из «1905», «~1918-1919 (убит)»; «XVI век», «?» → None."""
    m = re.search(r"\b(1[0-9]{3}|20[0-9]{2})\b", str(v or ""))
    return int(m.group(1)) if m else None


def is_open(p, now):
    b, d = year(p.get("born")), year(p.get("died"))
    return (b is not None and b < BORN_BEFORE) or (d is not None and d < now - DIED_YEARS)


def line(people, start, parent):
    chain, cur = [], start
    while cur:
        chain.append(people[cur])
        cur = people[cur].get(parent)
    chain.reverse()   # от вершины к --from
    # снизу вверх: как только встретился открытый, все выше тоже открыты
    flags, seen_open = [], False
    for p in reversed(chain):
        seen_open = seen_open or is_open(p, time.localtime().tm_year)
        flags.append(seen_open)
    return list(zip(chain, reversed(flags), strict=True))


def closed_label(rows, en):
    yrs = [y for p, _ in rows if (y := year(p.get("born")))]
    n = len(rows)
    if en:
        span = f", born {min(yrs)}–{max(yrs)}" if yrs else ""
        return f"🔒 {n} generation{'s' * (n != 1)}{span}: closed"
    few = 2 <= n % 10 <= 4 and n % 100 not in (12, 13, 14)
    word = "колено" if n % 10 == 1 and n % 100 != 11 else "колена" if few else "колен"
    span = f", род. {min(yrs)}–{max(yrs)}" if yrs else ""
    return f"🔒 {n} {word}{span}: закрыто"


def mermaid(rows, en):
    out, n, i = ["graph TD"], 0, 0
    while i < len(rows):
        p, ok = rows[i]
        if ok:
            out.append(f'  n{n}["{p["name"]}"]')
            i += 1
        else:
            run = [r for r in rows[i:] if not r[1]]
            out.append(f'  n{n}["{closed_label(run, en)}"]')
            i += len(run)
        if n:
            out.append(f"  n{n - 1} --> n{n}")
        n += 1
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", type=Path, default=Path("tree.yaml"),
                    help="файл дерева: people с id, name, born, died, father, mother")
    ap.add_argument("--from", dest="start", required=True, help="id в tree.yaml, от кого идти вверх")
    ap.add_argument("--line", choices=["father", "mother"], default="father")
    ap.add_argument("--list", action="store_true", help="списком, с пометкой открыт/закрыт")
    ap.add_argument("--en", action="store_true", help="подпись закрытого узла по-английски (для статьи)")
    a = ap.parse_args()
    people = {p["id"]: p for p in yaml.safe_load(a.tree.read_text())["people"]}
    if a.start not in people:
        sys.exit(f"нет id {a.start} в {a.tree}")
    rows = line(people, a.start, a.line)
    if a.list:
        for p, ok in rows:
            print(("открыт " if ok else "ЗАКРЫТ ") + f"{p.get('born', '?')!s:>10}  {p['name']}")
        print(f"{len(rows)} колен, открыто {sum(ok for _, ok in rows)}")
    else:
        print(mermaid(rows, a.en))


if __name__ == "__main__":
    main()
