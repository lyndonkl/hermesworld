import re
from pathlib import Path

def improve_skill(path, old_workflow_pattern, new_workflow):
    p = Path(path)
    content = p.read_text()
    
    # Remove the checklist parts
    content = re.sub(r'## Workflow\n\nCopy this checklist and track your progress.*?```(.*?)\n```', new_workflow, content, flags=re.DOTALL)
    content = re.sub(r'## Table of Contents.*?(?=## )', '', content, flags=re.DOTALL)
    
    p.write_text(content)

base = 'teams/exploratory/skills/cognitive-scaffolds/'

# brainstorm-diverge-converge
improve_skill(base + 'brainstorm-diverge-converge/SKILL.md', '',
'''## Procedure (Agent Execution)

Do not ask the user to copy checklists. You are an autonomous Hermes orchestrator. Maintain state internally and execute this scaffold across conversational turns:

1. **Diverge Phase:** When the user proposes a seed idea, immediately generate 5-7 radically divergent lateral options. Do not ask permission.
2. **Present & Clarify:** Present the clustered options. Ask the user **exactly one** clarifying question about which cluster to pursue. Wait for their response.
3. **Converge Phase:** Once they select a cluster, systematically prune the others. Generate a concrete synthesis of the winning direction.
4. **Handoff:** Suggest using `handoff-compaction` to formalize the result.
''')

# deliberation-debate-red-teaming
improve_skill(base + 'deliberation-debate-red-teaming/SKILL.md', '',
'''## Procedure (Agent Execution)

You are an autonomous Hermes orchestrator running a Socratic red-teaming session. Do not output checklists.

1. **Adopt Adversarial Stance:** When the user presents a plan, explicitly state the most catastrophic vulnerability or hidden assumption you see.
2. **The Debate Loop:** 
   - Attack one specific component of their plan.
   - Wait for their defense.
   - If their defense is weak, push harder. If it is strong, concede the point and attack the next vulnerability.
3. **One Question Constraint:** Never ask more than one question per turn. Force the user to resolve the contradiction before moving on.
4. **Synthesis:** Once all vectors are exhausted, produce a "Risk Register & Mitigations" summary.
''')

# cognitive-fallacies-guard
improve_skill(base + 'cognitive-fallacies-guard/SKILL.md', '',
'''## Procedure (Agent Execution)

Do not present menus or checklists to the user. When asked to audit a chart, presentation, or design, execute this silently and output the final audit:

1. **Scan for Misleads:** Identify chartjunk, 3D effects, and truncated axes.
2. **Cognitive Bias Check:** Analyze the text framing for confirmation bias and anchoring.
3. **Data Integrity:** Verify honest axes, fair comparisons, and context completeness.
4. **Output Report:** Generate a structured audit listing severity levels (High/Medium/Low) for each detected fallacy and specific mitigation recommendations.
''')

# socratic-teaching-scaffolds
improve_skill(base + 'socratic-teaching-scaffolds/SKILL.md', '',
'''## Procedure (Agent Execution)

Execute the teaching scaffold across multiple turns. Do not dump the entire curriculum at once.

1. **Diagnose:** Ask one probing question to identify the user's current knowledge level and misconceptions. Wait for response.
2. **Laddering:** Based on the response, design a progression. Provide a hint, analogy, or partial example (Scaffolding Level 4 or 3).
3. **Fade:** As the user gets it right, remove the scaffolding. Ask them to explain it back or solve a harder variant.
4. **Guardrail:** Never give the direct answer unless the user is completely stuck and frustrated. Always use the Socratic method to lead them to the "aha" moment.
''')

