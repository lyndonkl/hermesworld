---
name: markdown-to-pdf
description: Render a markdown report to PDF with pandoc and xelatex.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: writing
    tags: [PDF, Pandoc, LaTeX, Report Rendering]
    related_skills: [readability-check, term-interrogation]
---
# Markdown-to-PDF rendering

Converts a finished markdown report to a PDF using pandoc and the xelatex engine, with formatting
tuned for analyst-style output: letter paper, 1-inch margins, 11pt body, numbered footnotes, a
formal heading hierarchy. It does not install anything, does not pre-process the markdown, and
never modifies the input file. If pandoc or xelatex is missing it stops and prints the exact
install commands.

## When to Use

- Producing a finished strategist or analyst report PDF from a polished markdown source.
- The markdown uses pandoc-style footnotes (`[^1]`) and a YAML title block and needs a
  print-quality render.
- The last step of a report pipeline, after the prose passes and the readability score are done.
- Do not reach for it to install tooling or to reformat the document; it renders, and nothing
  else.

## Prerequisites

pandoc and a LaTeX engine (xelatex) must already be on the user's PATH. The user installs them
once; this skill never runs an installer. If either is missing, the checks below fail with the
install instructions and the run stops.

**macOS:**

```bash
brew install pandoc basictex
sudo tlmgr update --self
sudo tlmgr install xetex
```

`basictex` is about 90 MB. Do not install `mactex` unless the user specifically needs the full
LaTeX stack (around 5 GB).

**Linux (Debian/Ubuntu):**

```bash
sudo apt install pandoc texlive-xetex texlive-fonts-recommended
```

**Windows:** install pandoc from pandoc.org and MiKTeX (which provides xelatex); the render
command is the same.

After installation the user opens a new shell so `xelatex` is on PATH.

## How to Run

Every command below is run through `terminal`. Copy this checklist into the working response and
tick each step as it completes:

```
Markdown-to-PDF render:
- [ ] Step 1: Verify the input markdown file exists.
- [ ] Step 2: Verify pandoc is on PATH. If missing, print the pandoc install block and stop.
- [ ] Step 3: Verify xelatex is on PATH. If missing, print the xelatex install block and stop.
- [ ] Step 4: Create the output directory if it does not already exist.
- [ ] Step 5: Run the pandoc command exactly as specified below.
- [ ] Step 6: Confirm the output PDF file exists. Report its path.
```

### Step 2: verify pandoc

```bash
command -v pandoc
```

If this exits non-zero, print the block in "Failure messages" labelled *pandoc-missing* and stop.
Do not proceed to Step 5.

### Step 3: verify xelatex

```bash
command -v xelatex
```

If this exits non-zero, print the block in "Failure messages" labelled *xelatex-missing* and
stop. Do not proceed to Step 5.

### Step 5: the exact pandoc invocation

Run this with `terminal`. Substitute the input and output paths but do not modify any flag:

```bash
pandoc <INPUT_MD> \
  --from markdown+footnotes+yaml_metadata_block \
  --pdf-engine=xelatex \
  --output <OUTPUT_PDF> \
  --variable geometry:margin=1in \
  --variable papersize=letter \
  --variable fontsize=11pt \
  --variable linestretch=1.2 \
  --variable colorlinks=true \
  --variable linkcolor=black \
  --variable urlcolor=black \
  --variable toccolor=black
```

The variables are tuned for analyst-style output: letter-size paper, 1-inch margins, 11pt body at
1.2 line height, all hyperlinks rendered in black so the printed page reads cleanly.

## Failure messages

Print these blocks exactly as written. They are the contract with the user.

### pandoc-missing

```
ERROR: pandoc is not installed.

This skill requires pandoc and a LaTeX engine.

Install on macOS:
  brew install pandoc basictex
  sudo tlmgr update --self
  sudo tlmgr install xetex

Install on Linux (Debian/Ubuntu):
  sudo apt install pandoc texlive-xetex texlive-fonts-recommended

Open a new shell after installing so the new binaries are on PATH, then re-run.
```

### xelatex-missing

```
ERROR: xelatex is not installed.

pandoc is present, but the LaTeX engine (xelatex) is missing.

Install on macOS:
  brew install basictex
  sudo tlmgr update --self
  sudo tlmgr install xetex

Install on Linux (Debian/Ubuntu):
  sudo apt install texlive-xetex texlive-fonts-recommended

Open a new shell after installing, then re-run.
```

## Pitfalls

- The markdown source should use pandoc-style numbered footnotes: `text.[^1]` in the body with
  `[^1]: ...` definitions later in the file. These render as proper LaTeX footnotes. Inline
  `[Source: ...]` markers do not.
- If the markdown has a YAML front matter block with `title:`, `subtitle:`, and `date:` fields,
  those appear in the rendered title block. Without it the PDF has no title page.
- Do not pre-process the markdown. The pandoc invocation above is the only transformation.
- Auto-install of pandoc or LaTeX is explicitly out of scope. The skill never modifies the user's
  machine.
- A missing toolchain is not a failed run for the caller: the markdown is the deliverable. Report
  the install block alongside the markdown path and stop.

## Verification

```bash
test -s <OUTPUT_PDF> && echo "PDF rendered: <OUTPUT_PDF>"
```

If the output file does not exist or is empty after pandoc returns success, treat that as a
render failure and surface pandoc's stderr to the user.
