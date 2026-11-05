# shezhere

A Claude Code plugin for tracing Bashkir and South Ural ancestors in real archives, and for publishing
the old generations without exposing the living. The skills are written in Russian, because the
sources are.

Method, not a database: which archive answers, in what order to search, the traps we fell into, and
what an agent must never do on its own. Derived from a real family line traced to the 16th century.
Write-up: <https://rustman.org/wiki/genealogy-with-ai-agents>.

## Install

```
/plugin marketplace add fortunto2/shezhere
/plugin install shezhere@shezhere
```

## Skills

| Skill | What it covers |
|---|---|
| `shezhere` | revision lists (ревизские сказки), the 1917 census, Muslim metrical books in Arabic script, Pamyat Naroda and other military databases, kitaptar and ufagen, which province (губерния) holds your village, search traps, how to record a find, what to publish |
| `dna` | which test to take, known haplogroups of Bashkir clans, comparing with Bashkir projects, analysing your own WGS |

## Scripts

```bash
uv run scripts/tree-check.py --tree tree.yaml                    # duplicate ids, broken links, holes
uv run scripts/shezhere-public.py --tree tree.yaml --from <id>   # one line as Mermaid, living generations folded
```

`tree.yaml` is a flat list of people with `id`, `name`, `born`, `died`, `father`, `mother`, `spouse`
and a `note` that names its source. `examples/tree.yaml` is the public part of one paternal line, from
a printed shezhere, plus four placeholders the publishing rule has to close:

```bash
uv run scripts/shezhere-public.py --tree examples/tree.yaml --from descendant-4 --list
```

The publishing rule: a person is shown by name only if born before 1900 or dead for more than 75 years
(the term for which Russian archives close records of personal and family privacy, 125-FZ art. 25).
An ancestor of a shown person is shown too. Everyone else becomes one unnamed node.

## Open data from the same work

| Repository | What |
|---|---|
| [bashkir-genealogy-data](https://github.com/fortunto2/bashkir-genealogy-data) | index of the datasets, plus scripts for OBD Memorial, gwar.mil.ru, FamilySearch places and the Dresden POW database |
| [usergan-1920](https://github.com/fortunto2/usergan-1920) | 2,618 householders of the Usergan canton, 1920 census, with archive references. DOI [10.5281/zenodo.22747578](https://doi.org/10.5281/zenodo.22747578) |
| [orsk-uezd-ww1](https://github.com/fortunto2/orsk-uezd-ww1) | natives of Orsk uyezd in First World War records. DOI [10.5281/zenodo.23503840](https://doi.org/10.5281/zenodo.23503840) |

MIT licence for the skills and scripts. The datasets are CC BY 4.0.
