from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = PROJECT_ROOT / ".claude" / "skills" / "posit-project-profile" / "SKILL.md"


def load_project_profile(max_chars: int = 5000) -> str:
    if not PROFILE_PATH.exists():
        return ""
    text = PROFILE_PATH.read_text(encoding="utf-8").strip()
    if len(text) > max_chars:
        text = text[:max_chars].rsplit("\n", 1)[0] + "\n\n[project profile truncated]"
    return text
