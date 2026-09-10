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
| [`valuation-orchestrator`](packages/valuation-orchestrator/) + 14 specialist packages | The same valuation analysis as a **Bot team**: fifteen profiles, one per Claude agent, coordinated in the desktop's Bot Mode through `message_agent`. Each specialist keeps its own identity, memory, skills and model tier. Desktop only. | generated from the suite's briefs and finance skills |

## Prerequisites

- Hermes Agent 0.21 or newer, installed and already talking to a model. The
  desktop app installs the `hermes` CLI at `~/.local/bin/hermes`; check with
  `hermes --version`. If `hermes chat` does not work yet, finish `hermes setup`
  first: these packages reuse whatever model and credentials you already have.
- `git`, and `python3` with PyYAML (`python3 -m pip install pyyaml`). PyYAML is
  only needed by the repo tooling, not by the agents.
- Access to this repository (it is private at the moment).

## Quick start

```bash
git clone https://github.com/lyndonkl/hermesworld.git
cd hermesworld
tools/install.sh superforecaster       # one standalone agent
tools/install.sh --team valuation      # the fifteen-Bot valuation team (desktop Bot Mode)
tools/install.sh --all                 # everything
```

`tools/install.sh` runs `hermes profile install ./packages/<name> --alias --yes`
for each package. Every package ships a `config.yaml` that pins an OpenRouter
model chosen for its workload (the "balanced" preset in
[docs/MODELS.md](docs/MODELS.md)); if a package ever ships without one, the
installer copies the model block from your root profile instead.

Verify:

```bash
hermes profile list                    # one row per package, Distribution column filled
hermes -p superforecaster skills list  # 8 local skills, all enabled
hermes profile show superforecaster    # SOUL.md: exists, Distribution: superforecaster@1.0.0
```

Use:

```bash
superforecaster chat                   # the alias created by --alias
hermes -p valuation-suite chat         # the same thing without an alias
```

In the desktop app every installed profile appears in the profile rail and, with
Bot Mode on (Settings → Plugins → Bots), as a Bot in the roster: open its chat,
give it a title and avatar, seat it in a group chat, or `@mention` it from
another Bot's chat. Nothing extra to configure; a Bot is a profile.

The valuation **team** needs Bot Mode: open `valuation-orchestrator` from the Bots
roster and give it a company. It sends each stage to the right specialist Bot with
`message_agent`, which exists only in Bot Chats, and results come back between
turns. The team ships on the "balanced" model preset; switch presets any time:

```bash
python3 tools/team_models.py valuation --preset frontier    # or balanced | budget, or --show
```

See [packages/valuation-orchestrator/README.md](packages/valuation-orchestrator/README.md),
and [docs/MODELS.md](docs/MODELS.md) for which model fits which agent and why.

First prompts to try are in each package's README, for example
[packages/valuation-suite/README.md](packages/valuation-suite/README.md).

Optional, persistent memory across all profiles: a self-hosted Honcho stack whose
LLM work runs on a local model. One command, safe to re-run at any time; it checks
each step and skips what is already done:

```bash
tools/memory.sh --peer-name "Your Name"
```

It installs the local model server as a login agent (Apple Silicon; first run
downloads about 15 GB), starts Docker Desktop if needed, installs the Honcho CLI,
starts Honcho on port 8001, wires every installed profile to it, and prints a
status table. `tools/memory.sh` again later is the health check. Turn it off with
`python3 tools/memory_setup.py down --unwire`. Why Honcho, what it learns,
local-model options and costs: [docs/MEMORY.md](docs/MEMORY.md).

## Update, remove, and other install paths

```bash
git pull
hermes profile update superforecaster  # re-copies SOUL.md and skills; keeps your config, memories, sessions
hermes profile delete superforecaster  # removes the profile and its alias
```

Hermes installs a distribution from a git URL or a local directory and requires
`distribution.yaml` at the root of what it is given, with no sub-directory
syntax. That is why the commands above install from a local clone. If you want
`hermes profile install github.com/<owner>/hermes-<package>` to work,
`tools/publish_mirrors.sh <owner> --create` subtree-splits each package into its
own repository.

A single skill can also be installed on its own, straight from GitHub by path:

```bash
hermes skills install lyndonkl/hermesworld/packages/superforecaster/skills/forecasting/reference-class-forecasting
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| `hermes profile install` says "No distribution.yaml in ..." | Point it at `packages/<name>`, not the repo root |
| First chat says no model or provider is configured | `hermes -p <name> model`, or re-run `tools/install.sh <name>` after `hermes setup` on your root profile |
| The profile shows dozens of extra skills | `.no-bundled-skills` was deleted from the profile; that is fine, it just widens the skill index |
| `readability.py` exits asking for `textstat` | `python3 -m pip install --user textstat` (optional; the agents continue without it) |
| `product-strategist` cannot render a PDF | Install pandoc and a LaTeX engine (`brew install pandoc basictex` on macOS); markdown output is unaffected |
| A profile name collides with a command on your PATH | `hermes profile install ./packages/<name> --name <other-name>` |

## Two forms of the valuation analysis

| | `valuation-suite` (one profile) | Bot team (fifteen profiles) |
|---|---|---|
| Works in | CLI, desktop, gateways | Desktop Bot Chats only |
| Specialists are | stage briefs passed to anonymous `delegate_task` children | named Bots with their own SOUL, memory, skills, model tier |
| Dispatch | one call, several parallel tasks, structured results | one `message_agent` job per Bot, replies as notifications |
| Source of truth | the briefs and finance skills in `valuation-suite` | generated from the same files by `tools/build_team.py` |

## Documentation

- [AGENTS.md](AGENTS.md): the rules every package and skill follows, and the porting checklist.
- [docs/MODELS.md](docs/MODELS.md): where a model can be set, what each agent demands, the benchmark evidence, presets.
- [docs/MEMORY.md](docs/MEMORY.md): self-hosted Honcho memory on a local model, what each profile learns, limits.
- Each package's `README.md`: what it does, first prompts, its skills.

## What is in a package

```
packages/<name>/
  distribution.yaml      manifest (name, version, description, author, license)
  SOUL.md                the agent: identity and standing operating procedure
  config.yaml            model per workload (docs/MODELS.md), reasoning effort, cheap auxiliary model
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
python3 tools/build_team.py valuation                   # regenerate the team packages from the briefs
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
