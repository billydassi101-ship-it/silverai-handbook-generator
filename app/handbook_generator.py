import os
from app.llm_client import ask_llm_long
from app.config import OUTPUT_DIR

os.makedirs(OUTPUT_DIR, exist_ok=True)

HANDBOOK_SECTIONS = [
    "Introduction and Overview",
    "Core Concepts and Fundamentals",
    "Key Components and Architecture",
    "Implementation and Best Practices",
    "Use Cases and Applications",
    "Challenges and Limitations",
    "Advanced Topics and Future Directions",
    "Case Studies and Examples",
    "Tools and Frameworks",
    "Conclusion and Summary",
]


def generate_outline(topic: str, context: str) -> str:
    prompt = f"""
Based on the following context from uploaded documents, create a detailed outline for a comprehensive handbook about: {topic}

Context:
{context[:3000]}

Create a detailed outline with 10 chapters, each with 3-5 subsections.
Be specific and detailed.
"""
    return ask_llm_long(prompt)


def generate_section(
    topic: str,
    section: str,
    context: str,
    section_num: int,
    total: int
) -> str:
    prompt = f"""
You are writing a comprehensive professional handbook about: {topic}

Based on this context from source documents:
{context[:2500]}

Write Section {section_num}/{total}: {section}

Requirements:
- Write 1500 to 2000 words for this section
- Be detailed, professional, and informative
- Include examples, explanations, and insights
- Use markdown formatting with headers and subheaders
- Reference the uploaded source documents when relevant
- Do not invent citations or sources

Write the complete section now:
"""
    return ask_llm_long(prompt)


def generate_handbook(topic: str, context: str) -> str:
    print(f"Generating handbook on: {topic}")

    print("Generating outline...")
    outline = generate_outline(topic, context)

    handbook_parts = []

    handbook_parts.append(f"# {topic}\n\n")
    handbook_parts.append("## Table of Contents\n\n")

    for i, section in enumerate(HANDBOOK_SECTIONS, 1):
        handbook_parts.append(f"{i}. {section}\n")

    handbook_parts.append("\n---\n\n")
    handbook_parts.append(f"## Detailed Outline\n\n{outline}\n\n---\n\n")

    for i, section in enumerate(HANDBOOK_SECTIONS, 1):
        print(f"Generating section {i}/{len(HANDBOOK_SECTIONS)}: {section}")

        content = generate_section(
            topic=topic,
            section=section,
            context=context,
            section_num=i,
            total=len(HANDBOOK_SECTIONS),
        )

        handbook_parts.append(f"## {i}. {section}\n\n")
        handbook_parts.append(content)
        handbook_parts.append("\n\n---\n\n")

    handbook_parts.append(
        "## References\n\n"
        "This handbook was generated based on the uploaded source documents.\n"
    )

    full_handbook = "".join(handbook_parts)

    output_path = os.path.join(OUTPUT_DIR, "handbook.md")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_handbook)

    print(f"Handbook saved to {output_path}")
    print(f"Total words: {len(full_handbook.split())}")

    return full_handbook