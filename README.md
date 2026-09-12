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
| [`product-strategist`](packages/product-strategist/) | Reverse-engineers a real product's vision, strategy, and tactics from public material, grades every claim by evidence, and writes it for a reader with no background. | 11 skills: strategy and narrative methods, Damodaran strategy notes, layered reasoning, prose checks, PDF rendering |
| [`superforecaster`](packages/superforecaster/) | Calibrated probability forecasts: reference class first, Fermi decomposition, Bayesian updating, premortem, bias check. | 8 skills: 5 forecasting methods, voice and prose checks |
| [`cognitive-design-architect`](packages/cognitive-design-architect/) | Applies cognitive science to interfaces, data visualizations, educational content, and presentations, and explains why each choice works. | 8 skills: 6 design methods, prose checks |
| [`geometric-deep-learning-architect`](packages/geometric-deep-learning-architect/) | Symmetry discovery, group identification, and equivariant neural-network design and audit. | 7 skills: 5 geometric deep learning methods, prose checks |
| [`valuation-orchestrator`](packages/valuation-orchestrator/) and 14 specialist Bots | Company valuation and corporate-finance analysis as a **team of fifteen agents**: the orchestrator fixes the mandate, sends each stage to the right specialist, checks every gate, and hands over the verdict. Six modes: valuation, corporate-finance, acquisition, project, ipo, restructuring. Each specialist also works on its own. | 19 finance skills with tested Python engines, 14 stage briefs, the Damodaran playbooks |

## Prerequisites

- Hermes Agent 0.21 or newer, installed and already talking to a model. The
  desktop app installs the `hermes` CLI at `~/.local/bin/hermes`; check with
  `hermes --version`. If `hermes chat` does not work yet, finish `hermes setup`
  first: these packages reuse whatever model and credentials you already have.
- `git`, and `python3` with PyYAML (`python3 -m pip install pyyaml`). PyYAML is
  only needed by the repo tooling, not by the agents.
- An OpenRouter API key already set up in Hermes (the packages pin OpenRouter
  models; change them with `hermes -p <name> model` if you use another provider).
- For the optional memory stack only: Docker Desktop (the script starts it) and
  [`uv`](https://docs.astral.sh/uv/) (the script uses it to install the Honcho CLI).
  Honcho's own model calls go to OpenRouter with the same key; nothing runs on
  your GPU.

## Quick start

```bash
git clone https://github.com/lyndonkl/hermesworld.git
cd hermesworld
tools/install.sh superforecaster       # one standalone agent
tools/install.sh --team valuation      # the fifteen-agent valuation team
tools/install.sh --all                 # everything
```

`tools/install.sh` runs `hermes profile install ./packages/<name> --alias --yes`
for each package. Every package ships a `config.yaml` that pins an OpenRouter
model chosen for its workload (the "balanced" preset in
[docs/MODELS.md](docs/MODELS.md)). Hermes profiles are credential-isolated, so
the installer also copies the pinned provider's API key from your root
`~/.hermes/.env` into each new profile's own `.env`, locally and with mode 600.
No key is ever part of this repository. Some OpenRouter models, Meta's Muse
Spark among them (offered here as the `spark` preset), need a one-time 18+
confirmation in your OpenRouter account settings before they answer.

Verify:

```bash
hermes profile list                    # one row per package, Distribution column filled
hermes -p superforecaster skills list  # 9 local skills (8 of ours plus Hermes's own hermes-agent), all enabled
hermes profile show superforecaster    # SOUL.md: exists, Distribution: superforecaster@1.0.0
```

Use a standalone agent, in a terminal or in the desktop app:

```bash
superforecaster chat                   # the alias created by --alias
hermes -p product-strategist chat      # the same thing without an alias
```

In the desktop app every installed agent appears in the profile list on the left.
With **Bot Mode** switched on (Settings → Plugins → Bots) they also appear as Bots
with a title and avatar, and you can `@mention` one from another's chat or seat
several in a group chat.

Start the valuation team:

```bash
valuation                              # terminal: opens the orchestrator's Bot Chat
valuation --tui                        # the same in the Ink terminal UI
```

or, in the desktop app, switch Bot Mode on and click **valuation-orchestrator** in
the Bots list. Give it a company and a question, for example "Value Costco as of
last Friday's close, in USD." It asks what it cannot infer, then sends each stage
to the right specialist; the answers come back into its chat as notifications, so
you will see it dispatch, pause, and continue. You can switch to other chats while a
stage runs. Close the specialists' chats before you start, and leave them closed until
the run reports back: a specialist whose chat is open when its job arrives works inside
that chat instead, and the orchestrator stops waiting for the answer after five minutes.
Open a specialist's chat afterwards to read what it did. Use either the desktop or the
terminal for the orchestrator, not both at once; the second one is refused with
"already has a live owner". The desktop keeps only three profile backends running at
a time (Settings, pool limits), and every Bot chat you open takes one.
A specialist can also be asked directly, for example
`cost-of-capital-analyst chat` and "estimate Costco's cost of capital"; it will
ask for the inputs it needs.

## Words used here

- **Profile.** One installed agent: its personality file (`SOUL.md`), its skills,
  its memory, its model, and its own API key file. Each has a name and a command,
  and lives in `~/.hermes/profiles/<name>/`.
- **Bot.** What the desktop app calls a profile when Bot Mode is on. Same thing.
  Installing a team marks its profiles as Bots, so the desktop lists them and
  teammate messaging works; there is nothing to configure.
- **Bot Chat.** Every Bot has one permanent main conversation with that name. It
  is the only conversation in which a Bot can message other Bots, and it is where
  teammates' messages arrive. In the desktop you are in it as soon as you click a
  Bot. In a terminal you open it by name, which is all the `valuation` command
  does: `hermes -p valuation-orchestrator chat -c "Bot Chat" --create-if-missing`.
  A plain `valuation-orchestrator chat` opens an ordinary conversation instead, and
  the orchestrator will tell you it cannot reach its team from there.
- **Teammate message.** One Bot writing to another, like texting a colleague. The
  sender carries on; the other Bot does the work in its own Bot Chat, and its reply
  arrives back in the sender's chat as a notification when it is done. Hermes
  delivers these on your machine; the desktop app can also relay them to Bots on
  other machines, which this repo does not use.
- **Orchestrator, specialist, job, workspace.** The orchestrator owns the
  conversation with you and the run's folder on disk (the workspace, one numbered
  sub-folder per stage). A job is the short message it sends a specialist: what to
  do, which files to read and write, the constraints, the currency and date. A
  specialist is a Bot that does one stage and writes only its own files.

Optional, persistent memory across all profiles: a self-hosted Honcho stack in
Docker, with its model calls on cheap OpenRouter models. One command, safe to
re-run at any time; it checks each step and skips what is already done:

```bash
tools/memory.sh --peer-name "Your Name"
```

It starts Docker Desktop if needed, installs the Honcho CLI, starts Honcho on port
8001, wires every installed profile to it, and prints a status table. Running
`tools/memory.sh` again later is the health check. Turn it off with
`python3 tools/memory_setup.py down --unwire`. Why Honcho, what it learns, which
models it uses and what they cost: [docs/MEMORY.md](docs/MEMORY.md).

## Update, remove, and other install paths

```bash
git pull
hermes profile update superforecaster  # re-copies SOUL.md and skills; keeps your config, memories, sessions
hermes profile update superforecaster --force-config   # also re-applies the shipped config.yaml
hermes profile delete superforecaster  # removes the profile and its alias
rm ~/.local/bin/valuation              # the team command is ours, not Hermes's; remove it by hand
```

An update replaces the whole `skills/` folder, so a skill the agent saved into the
profile itself is removed; keep such skills in your root profile instead.

```bash
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
| The orchestrator's chat says it `already has a live owner` | It is open somewhere else (the desktop or a terminal). Close it there, then retry |
| Clicking a Bot in the desktop does nothing for a while | The desktop keeps only three profile backends warm and queues the rest. Raise **Warm bot backends** under Settings, Advanced (8 is plenty), or wait a minute after a restart |
| A Bot keeps asking you to approve commands | Hermes's security scan escalates script-style commands. Type `/yolo` in that chat to auto-approve for the session, or pick "Always approve" on the prompt. `approvals.mode: off` in a profile's `config.yaml` turns the checks off for that profile |
| In the desktop, a new chat shows a different model than the profile pins | The desktop's composer remembers the last model you picked and applies it to every new chat, silently, without changing the profile. Click the model pill in the composer and pick the profile's model (or its default entry); the profile's `config.yaml` was never changed. `hermes profile show <name>` prints the pinned model |

## What is in a package

```
teams/valuation/         the team's source of truth: team.yaml plus the 19 finance skills
                         and 14 stage briefs; tools/build_team.py generates the 15 packages
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
