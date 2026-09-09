from __future__ import annotations

import secrets
from pathlib import Path


def _read_value(content: str, key: str) -> str:
    prefix = f"{key}="
    for line in content.splitlines():
        if line.startswith(prefix):
            return line[len(prefix) :].strip().strip('"').strip("'")
    return ""


def _write_value(content: str, key: str, value: str) -> str:
    prefix = f"{key}="
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = f'{key}="{value}"'
            break
    else:
        lines.append(f'{key}="{value}"')
    return "\n".join(lines) + "\n"


def prepare_env(root: Path) -> bool:
    env_path = root / ".env"
    example_path = root / ".env.example"
    if env_path.exists():
        content = env_path.read_text(encoding="utf-8")
    elif example_path.exists():
        content = example_path.read_text(encoding="utf-8")
    else:
        raise FileNotFoundError(".env.example was not found")

    if _read_value(content, "DJANGO_SECRET_KEY"):
        return False

    content = _write_value(content, "DJANGO_SECRET_KEY", secrets.token_urlsafe(50))
    env_path.write_text(content, encoding="utf-8")
    return True


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    created = prepare_env(root)
    if created:
        print("Created or completed the ignored .env with a generated local Django secret.")
    else:
        print("Existing non-empty Django secret preserved in .env.")


if __name__ == "__main__":
    main()