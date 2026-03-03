---
name: create-tech-illustration
description: Generate schematic analogy infographic prompts from technical articles. Analyzes text for inefficiencies/mismatches and produces engineering-blueprint style image prompts for Nano Banana Pro.
---

# Schematic Analogy Infographic Generator

## Purpose

Analyze a technical article and generate distinct image-generation prompts for Nano Banana Pro. Each prompt describes a high-fidelity, engineering-blueprint infographic that visualizes a technical mismatch or inefficiency from the text.

## Configurable Parameters

Collect these from the user (or use defaults):

| Parameter | Default |
|-----------|---------|
| Total Prompts [N] | 3 |
| Resolution | Native 4K |
| Accent Color | Cobalt Blue |

## Style Specifications

Every prompt MUST follow this aesthetic:

- **Aesthetic:** Professional CAD/technical drafting. High-precision black vector line art on clean white vellum background with subtle grey technical grid.
- **Layout:** Highly Complex Machine (over-engineered solution) on the LEFT. Basic Utility Object (simple task) on the RIGHT.
- **Header:** Bold, heavy sans-serif analogy title at top center.
- **Data Callouts:** Small, monospaced "coding" font labels (e.g., `"$15/M TOKENS"`, `"1.5T PARAMS"`) positioned along dimension lines.
- **Diagrammatic Elements:** Witness lines, dimension arrows, dashed horizontal alignment lines. Dashed vertical borders on far left/right margins to simulate an official technical document.
- **The Connector:** A large, solid directional arrow in the [Accent Color] pointing from the complex machine toward the simple object.

## Conceptual Frameworks

For each of the [N] prompts, identify a unique inefficiency from the article and apply one of these frameworks:

1. **Financial Malpractice** — Focus on "Cost vs. Utility"
2. **Structural Overkill** — Focus on "Complexity vs. Requirement"
3. **Signal vs. Noise** — Focus on "Massive Input vs. Minimal Output"

## Output Format

For each prompt, provide:

1. **The Logic:** A brief explanation of the specific article insight being visualized.
2. **The Nano Banana Pro Prompt:** A detailed, ready-to-use prompt including resolution and specific text strings in quotes.

## Workflow

1. Read the provided article.
2. Identify [N] distinct inefficiencies or mismatches.
3. Map each to a conceptual framework.
4. Craft an analogy title (the header) as a vivid metaphor (e.g., "BUILDING AN AIRPORT TO CROSS THE STREET").
5. Write the full prompt with LEFT (complex) and RIGHT (simple) elements, data callouts, and accent color arrow.
6. Generate 1K drafts first using Nano Banana Pro for review.
7. On user approval, regenerate selected prompts at final resolution (default 4K).
