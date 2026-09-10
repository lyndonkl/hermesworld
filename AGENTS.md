# hermesworld — conventions for editing this repo

This monorepo holds **Hermes Agent profile distributions**: each directory under
`packages/` is a complete, installable Hermes agent (persona + skills + config).
The agents were ported from a Claude Code plugin; this file records the rules
every package and skill must satisfy so the port stays faithful to the Hermes
runtime. The rules were taken from the Hermes source (v0.21.1), not guessed:
`hermes_cli/profile_distribution.py`, `tools/skill_manager_tool.py`,
`tools/skill_linter.py`, `tools/skills_guard.py`, `agent/skill_utils.py`,
`skills/AGENTS.md`, and `CONTRIBUTING.md` ("Skill authoring standards").

Run `python3 tools/validate.py --selftest`, `python3 tools/sync_shared.py --check`
and `python3 tools/build_team.py --check` before committing. Zero errors is the bar. `python3 tools/validate.py --hermes-src ~/.hermes/hermes-agent` also
runs Hermes's own linter when a checkout is available.

## Layout

```
packages/<name>/                 one Hermes distribution (installable directory)
                                 (team members are generated: see "Bot teams" below)
teams/<team>/team.yaml           manifest for a Bot team: orchestrator, members, tiers, models
teams/<team>/skills/             the team's canonical skills and stage briefs
  distribution.yaml              manifest: name (== dir), version, description, author, license
  SOUL.md                        the agent: identity + standing operating procedure
  config.yaml                    model + effort per workload (docs/MODELS.md), cheap auxiliary model
  README.md                      human-facing: what it does, install, first prompts
  .gitignore                     runtime files that must never ship
  shared-skills.txt              "<category>/<skill>" lines copied from shared/skills/
  skills/<category>/DESCRIPTION.md   frontmatter `description:` for the category
  skills/<category>/<skill>/SKILL.md [+ scripts/ references/ templates/ assets/]
shared/skills/<skill>/           canonical copy of any skill used by more than one package
tools/                           validate.py, sync_shared.py, build_team.py, team_models.py,
                                 install.sh, post_install.py, publish_mirrors.sh,
                                 convert_claude_skill.py, memory.sh (+ memory_setup.py)
infra/honcho/                    Honcho env template rendered by memory_setup.py
docs/                            MODELS.md (model choices), MEMORY.md (Honcho memory set-up)
```

Hard constraints from the installer: `distribution.yaml` must be at the package
root; **no symlinks anywhere** (the install is refused); anything named like runtime
state (`.env`, `auth.json`, `memories/`, `sessions/`, `logs/`, `cache/`, `local/` ...)
is silently stripped at install, so never ship anything that relies on it.

## Skills

A skill is `skills/<category>/<name>/SKILL.md`. Category is one folder level;
Hermes derives the category from the path, so `metadata.hermes.category` (when
present) must equal the folder name. Support directories are exactly
`scripts/`, `references/`, `templates/`, `assets/` — nothing else (Hermes only
lists and serves those; the Claude `resources/` layout is not one of them).

### Frontmatter (all fields required in this repo)

```yaml
---
name: dcf-valuation-engine            # == directory name; [a-z0-9][a-z0-9_-]*
description: "Run a DCF from drivers to value per share and implied expectations."
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]    # scripts here are stdlib Python; declare all three
metadata:
  hermes:
    category: corporate-finance        # == folder; omit only for shared skills
    tags: [Valuation, DCF, Corporate Finance]
    related_skills: [valuation-consistency-checks, cost-of-capital-toolkit]
---
```

- `description`: **at most 60 characters**, one sentence, capability first,
  ends with a period, no marketing words (powerful, comprehensive, seamless,
  advanced, robust, cutting-edge, state-of-the-art, revolutionary), does not
  repeat the name. Quote it if it contains a colon. Hermes shows a description
  of up to 60 characters whole and cuts a longer one to 57 plus an ellipsis in
  the skill index; the trigger must fit.
- `tags`: 3–6 Title-Case terms someone would search for.
- `related_skills`: names of skills that ship in the **same package** (or in
  `shared/skills/`). The validator rejects anything else.

### Body

Section order, adapted from Hermes's "modern section order" for method skills:

1. `# <Title>` then a 2–3 sentence intro: what it does and what it does not do.
2. `## When to Use` — 3–6 trigger bullets. Fold the old long Claude description
   ("Use when ...") in here; it carries the routing phrases.
3. For script-backed skills: `## Prerequisites` (usually "Python 3, stdlib
   only"), `## How to Run`, `## Quick Reference`.
4. `## Procedure` / the method, `## Pitfalls`, `## Verification` (the one
   command that proves it works, e.g. a `selftest`).

Keep SKILL.md around 100–300 lines. Bulk (worked examples, catalogues, long
tables) goes to `references/<topic>.md` and is pointed at, not inlined:
`skill_view("dcf-valuation-engine", file_path="references/worked-examples.md")`.
Only top-level `references/*.md` are advertised to the agent, so keep
references flat. Cross-skill loads (`skill_view("valuation-playbooks",
file_path="references/x.md")` from another skill) are resolved against the named
skill by `tools/validate.py`; Hermes's own linter cannot see the skill name and
reports them as advisory `dangling-reference` warnings, which is expected.

Scripts are invoked with the absolute-path token Hermes substitutes at view
time, wrapped as a `terminal` call in prose:

```bash
python3 ${HERMES_SKILL_DIR}/scripts/dcf.py value --in drivers.json
```

Cross-skill scripts: `${HERMES_SKILL_DIR}/../<sibling-skill>/scripts/x.py`
(siblings share a category folder). Data files live beside their script under
`scripts/data/`; scripts locate them relative to `__file__`.

Never ship inside a skill: `README.md`, `CHANGELOG.md`, `install.sh`, `.env`,
`.gitignore`, hooks, binaries, `.DS_Store`.

### Tool vocabulary

Prose names Hermes tools in backticks, never Claude Code tools or wrapped
shell utilities.

| Claude Code | Hermes |
|---|---|
| `Read` | `read_file` |
| `Write` / `Edit` | `write_file` / `patch` |
| `Bash` | `terminal` |
| `Glob`, `Grep` | `search_files` |
| `WebSearch` | `web_search` |
| `WebFetch` | `web_extract` |
| `AskUserQuestion` | `clarify` |
| `Skill` tool / `/skill` | `skill_view` |
| `Agent` / `Task` tool, `subagent_type` | `delegate_task` |
| `TodoWrite` | `todo_list` (the tool; `todo` is only the toolset name) |
| `$ARGUMENTS` | "the user's instruction" (Hermes appends it after `/name`) |
| `grep`, `cat`, `head`, `tail`, `sed`, `awk`, `find`, `ls` in prose | `search_files`, `read_file`, `patch` |
| `knowledge/...`, `resources/...` paths | bundled `references/...` inside a skill |

Shell commands inside fenced code blocks are fine (the agent runs them through
`terminal`); the rule is about prose.

## SOUL.md (the agent)

Hermes injects `SOUL.md` verbatim as slot #1 of the system prompt for every
session of the profile. It is distribution-owned, so it is replaced on
`hermes profile update` (unlike `config.yaml`, which installers keep). That
makes it the right home for the agent's identity **and** its standing
operating procedure — the equivalent of a Claude subagent's body.

Rules:

- Open with who the agent is and what it refuses to do, then the workflow.
  Keep the file under ~400 lines; move reference material into skills.
- Refer to skills by name and say when to load them: "Load
  `reference-class-forecasting` with `skill_view` before step 2."
- Use `clarify` for genuine choices, `web_search` / `web_extract` for research,
  `write_file` for deliverables, `terminal` for scripts.
- Delegated children (`delegate_task`) do **not** see SOUL.md and have no
  conversation history. Anything a child must know goes into its `goal` and
  `context`, including which skill to `skill_view` and the absolute paths to
  read and write. Children cannot call `clarify`; questions come back through
  the parent.
- No per-role model tiers (Claude's `model: opus|sonnet`): Hermes picks the
  model from the profile's config, and children inherit it.
- No Claude-isms (see the vocabulary table), no `knowledge/` or `resources/`
  paths, no machine-local paths.

## Bot teams (generated packages)

A team is one profile per agent, coordinated in the desktop's Bot Mode through the
`message_agent` tool (fire-and-forget, 16,000-character messages, one job per Bot at a
time, replies arrive as background completion notifications; Bot Chats only). Each team
is described by `teams/<team>/team.yaml` and generated by `python3 tools/build_team.py`:

- Canonical sources live in `teams/<team>/skills/`: the stage briefs under
  `valuation-specialists/` and the finance skills under `corporate-finance/`. Edit
  those, then rebuild. They are validated through the generated packages.
  Never edit a generated member package by hand; `tools/build_team.py --check` fails
  on drift and CI runs it.
- A member package gets `SOUL.md` (team preamble + the brief from `## Role` on),
  `bot.yaml` (title, tier, roster description; `tools/install.sh` writes it into the
  profile's `profile.yaml` once, which is what makes the profile a Bot), its brief as
  a skill, and its finance skills plus the dependency closure the generator computes.
- The team orchestrator's `SOUL.md` and `README.md` are hand-written; the rest of
  its package is generated. It differs from the single-profile suite's SOUL only in
  the dispatch mechanics (job envelope + `message_agent` instead of `delegate_task`).
- The orchestrator's generated `config.yaml` sets `dashboard.ws_orphan_reap_grace_s: 0`.
  The desktop backend otherwise unloads a Bot Chat 20 s after the app stops showing it, and
  unloading kills the session's background processes, which is where a `message_agent`
  delivery and the teammate turn inside it run (Hermes `tui_gateway/session_lifecycle.py`,
  `agent/client_lifecycle.py`; the kill also discards the failure notice). The setting is
  read once, at backend start, from the config of the profile the backend was launched
  with; the desktop launches one backend per profile, so the orchestrator's own config is
  the right place, but a single multiplexed backend would need it in its launch profile
  (or the env var `HERMES_TUI_WS_ORPHAN_REAP_GRACE_S`). Zero means a detached session is
  never unloaded, which can leave one idle helper process per dashboard refresh. Config
  changes reach existing installs through `tools/install.sh` or `hermes profile update
  <name> --force-config`; a plain `hermes profile update` keeps the installed `config.yaml`.
- The sender receives only the last 2,000 characters of a teammate's answer
  (`tools/process_registry.py`), so briefs end with the status line and the member preamble
  caps answers at 1,500 characters. A local delivery failure is a JSON object with `error`
  and `reason` fields in the notification output; the `[reason: <code>]` tag exists only for
  cross-machine relay. Hermes injects its own messaging protocol into every Bot Chat prompt,
  including "reply via message_agent"; the member preamble overrides that for jobs, and
  `agent.bot_mode_protocol` stays on so members keep the tool for anything else.
- The delivery path is chosen when a job is sent. A teammate whose Bot Chat is open in the
  desktop at that moment gets the job through Hermes's live path, whose sender-side wait is
  capped at 300 s; after that the orchestrator receives a `queued` notice instead of the
  answer. A chat opened after the job started is refused as busy. The docs tell users to
  close specialist chats before a run.
- A job turn is a one-shot CLI turn (`hermes chat -Q --query-file`): `clarify` is answered
  by Hermes with "make an assumption" (a silent guess), destructive commands are denied
  rather than asked (`approvals.single_query_mode`), `terminal` commands time out at 180 s
  by default, and a background process's result never reaches a one-shot. The member
  preamble carries these rules; the orchestrator SOUL says teammates must not ask.
- Every constant the team relies on (16,000-character messages, the 300 s live wait, the
  2,000-character tail, the 20 s reap grace) is a Hermes internal, not a documented
  promise; re-check them against the source after a Hermes update.
- Hermes's Kanban board (`hermes kanban`, dispatcher inside the messaging gateway) is the
  documented mechanism for this shape of work: durable tasks, parent links for ordering, a
  review lane, workers spawned as the assigned profile with its SOUL, skills and model. It
  was not weighed when the team was built and needs `hermes gateway start` running; it is
  the candidate replacement for the `message_agent` dispatch if that proves too fragile.
- Tiers (`orchestrator`/`strong`/`fast`/`writer`) mirror the work each agent does; the
  manifest's `models:` map pins one OpenRouter model per tier into generated configs. `tools/team_models.py --preset frontier|balanced|budget` applies
  models per tier to installed profiles; the picks and their benchmark basis are in
  `docs/MODELS.md` (dated; re-check before changing them).

## Memory (Honcho, self-hosted)

Memory is user-owned and never ships in a package. `tools/memory.sh` (idempotent) stands up a
self-hosted Honcho stack whose LLM jobs run on OpenRouter models (GLM-5.3-Flash for the
high-volume jobs, GLM-5.3 for deep dialectic, `openai/text-embedding-3-small` for vectors),
then wires every installed hermesworld profile to it: one shared user peer, one AI peer
per profile, strong-persona observation for the specialist Bots. The env template is
`infra/honcho/honcho.env.template`; the reasoning and limits are in `docs/MEMORY.md`.
Only one external memory provider can be active per profile.

## Shared skills

Skills used by more than one package live once in `shared/skills/<skill>/` and
are copied into each package by `python3 tools/sync_shared.py`, driven by the
package's `shared-skills.txt`. Edit only the canonical copy; the validator fails
on drift. Shared skills omit `metadata.hermes.category` because their folder
differs per package.

## Porting checklist (Claude Code → Hermes)

1. `python3 tools/convert_claude_skill.py <claude-skill> packages/<pkg>/skills/<cat>/<skill> --category <cat>`
   moves `resources/` into the Hermes support dirs and rewrites paths.
2. Write the ≤60-char description, tags, related_skills; turn the draft
   `## When to Use` into trigger bullets and delete the `CONVERT` comment.
3. Replace Claude tool names; bundle any `knowledge/` files as references.
4. For an agent: write `SOUL.md` from the Claude agent body; write
   `distribution.yaml`, `config.yaml`, `README.md`, category `DESCRIPTION.md`.
5. `python3 tools/validate.py --selftest` → 0 errors; then
   `tools/install.sh <pkg>` and try it: `hermes -p <pkg> chat`.
