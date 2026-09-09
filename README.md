# hermesworld

Hermes Agent profile distributions, one per directory under `packages/`. Each
package is a complete agent: a `SOUL.md` that carries its identity and
operating procedure, the skills it works with, and behavioural defaults.
Install one and you get a named Hermes profile you can chat with from the CLI,
the desktop app, or any gateway platform.

These agents were ported from the Claude Code plugin at
[lyndonkl/claude](https://github.com/lyndonkl/claude). The port follows the
Hermes rules taken from its source (v0.21.1) rather than from memory; the
rules are written down in [AGENTS.md](AGENTS.md) and enforced by
`tools/validate.py`.

## Packages

| Package | What it does | Skills |
|---|---|---|
| [`valuation-suite`](packages/valuation-suite/) | Company valuation and corporate-finance analysis. One profile: an orchestrator that classifies the company, runs 14 specialist stages through `delegate_task`, and reconciles a verdict. Six modes: valuation, corporate-finance, acquisition, project, ipo, restructuring. | 35 skills: 19 finance skills (11 with tested stdlib-Python engines), 14 stage briefs, the Damodaran playbooks, readability check |
| [`product-strategist`](packages/product-strategist/) | Reverse-engineers a real product's vision, strategy, and tactics from public material, grades every claim by evidence, and writes it for a reader with no background. | 11 skills: strategy and narrative methods, Damodaran strategy notes, layered reasoning, prose checks, PDF rendering |
| [`superforecaster`](packages/superforecaster/) | Calibrated probability forecasts: reference class first, Fermi decomposition, Bayesian updating, premortem, bias check. | 8 skills: 5 forecasting methods, voice and prose checks |
| [`cognitive-design-architect`](packages/cognitive-design-architect/) | Applies cognitive science to interfaces, data visualizations, educational content, and presentations, and explains why each choice works. | 8 skills: 6 design methods, prose checks |
| [`geometric-deep-learning-architect`](packages/geometric-deep-learning-architect/) | Symmetry discovery, group identification, and equivariant neural-network design and audit. | 7 skills: 5 geometric deep learning methods, prose checks |

## Install

Hermes installs a distribution from a git URL **or a local directory**, and it
requires `distribution.yaml` at the root of whatever it is given. A monorepo
sub-directory therefore installs from a local clone:

```bash
git clone https://github.com/lyndonkl/hermesworld.git
cd hermesworld
tools/install.sh superforecaster            # one package
tools/install.sh --all                      # every package
```

`tools/install.sh` runs `hermes profile install ./packages/<name> --alias --yes`
and then seeds the new profile's model block from your root profile, because
packages deliberately do not pin a model or provider. Equivalent by hand:

```bash
hermes profile install ./packages/superforecaster --alias
hermes -p superforecaster model          # pick the model if none was seeded
superforecaster chat                     # or: hermes -p superforecaster chat
```

Updating later:

```bash
git pull
hermes profile update superforecaster    # re-copies SOUL, skills, cron; keeps your config, memories, sessions
```

Installing a single skill instead of a whole agent also works, straight from
GitHub by path:

```bash
hermes skills install lyndonkl/hermesworld/packages/superforecaster/skills/forecasting/reference-class-forecasting
```

If you ever want `hermes profile install github.com/...` for a package,
`tools/publish_mirrors.sh <owner>` subtree-splits each package into its own
`hermes-<package>` repository, whose root is the package.

## What is in a package

```
packages/<name>/
  distribution.yaml      manifest (name, version, description, author, license)
  SOUL.md                the agent: identity and standing operating procedure
  config.yaml            behavioural defaults; no model pin (installers keep their own)
  README.md              what it does, install, first prompts
  .no-bundled-skills     keeps the profile's skill index focused on this agent; delete to opt back in
  shared-skills.txt      skills copied in from shared/skills/
  skills/<category>/DESCRIPTION.md
  skills/<category>/<skill>/SKILL.md  (+ scripts/ references/ templates/ assets/)
```

Skills used by more than one package are authored once under `shared/skills/`
and copied into each package by `tools/sync_shared.py`, because a distribution
must be self-contained and may not contain symlinks.

## Working on the repo

```bash
python3 tools/validate.py --selftest                    # every rule in AGENTS.md, plus script selftests
python3 tools/sync_shared.py                            # propagate shared skills
python3 tools/validate.py --hermes-src ~/.hermes/hermes-agent   # also run Hermes's own skill linter
python3 tools/convert_claude_skill.py <claude-skill-dir> packages/<pkg>/skills/<cat>/<skill> --category <cat>
```

Read [AGENTS.md](AGENTS.md) before adding or changing anything; it is the spec
the validator enforces and the checklist for porting further Claude Code
agents.

## How the Claude Code concepts map to Hermes

| Claude Code | Hermes, in this repo |
|---|---|
| Subagent file in `agents/*.md` | The profile's `SOUL.md` (identity + procedure, injected as slot 1 of the system prompt) |
| `skills:` frontmatter on an agent | Skills shipped in the package; the SOUL says when to load each with `skill_view` |
| `Agent(...)` fan-out to named specialists | `delegate_task` with the specialist's stage brief (a skill) passed as the child's `context` |
| `resources/` inside a skill | `scripts/`, `references/`, `templates/`, `assets/` |
| `python3 resources/x.py` | `python3 ${HERMES_SKILL_DIR}/scripts/x.py` (Hermes substitutes the absolute path) |
| `AskUserQuestion`, `WebSearch`, `WebFetch`, `Read`, `Write`, `Bash` | `clarify`, `web_search`, `web_extract`, `read_file`, `write_file`, `terminal` |
| `model: opus` per agent | One model per profile; children inherit it (or `delegation.model`) |
| `knowledge/` notes | Bundled as `references/` inside a skill |
| Stop / PostToolUse hooks | Not ported; the readability check runs on demand |

## License

MIT. See [LICENSE](LICENSE).
