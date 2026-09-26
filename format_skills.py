import re
import sys
from pathlib import Path

def format_skill(path, desc, tags):
    p = Path(path)
    content = p.read_text()
    
    # Replace description
    content = re.sub(r'description:.*?(?=\n---|\n[a-z])', f'description: "{desc}"', content, flags=re.DOTALL)
    
    # Ensure tags exist under metadata.hermes
    if 'tags:' not in content:
        if 'category: cognitive-scaffolds' in content:
            content = content.replace('category: cognitive-scaffolds', f'category: cognitive-scaffolds\n    tags: {tags}')
    
    p.write_text(content)

base = 'teams/exploratory/skills/cognitive-scaffolds/'
format_skill(base + 'brainstorm-diverge-converge/SKILL.md', 'Facilitate divergent brainstorming followed by convergence.', '[Ideation, Brainstorming, Scaffolds]')
format_skill(base + 'cognitive-fallacies-guard/SKILL.md', 'Audit visualizations for cognitive fallacies and misleads.', '[Design, Fallacies, Audit]')
format_skill(base + 'deliberation-debate-red-teaming/SKILL.md', 'Run a structured red-teaming debate to test hypotheses.', '[Debate, Red Teaming, Logic]')
format_skill(base + 'socratic-teaching-scaffolds/SKILL.md', 'Guide users through Socratic teaching and scaffolding.', '[Socratic, Teaching, Scaffolds]')
