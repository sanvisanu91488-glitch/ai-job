
import fitz


def extract_resume_text(file_bytes):
    text_parts = []

    with fitz.open(stream=file_bytes, filetype="pdf") as pdf:
        for page in pdf:
            text_parts.append(page.get_text())

    return "\n".join(text_parts)


def extract_known_skills(text, known_skills):
    text_lower = text.lower()

    found = []

    for skill in known_skills:
        if skill.lower() in text_lower:
            found.append(skill)

    return sorted(set(found))
