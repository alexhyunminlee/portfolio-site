"""
Content loader — merges all YAML files from content/ into a single dict.

Load order:
  1. content/profile.yaml           — site-wide identity (name, bio, social)
  2. content/professional/*.yaml    — professional experience, education, projects, skills
  3. content/personal/*.yaml        — personal projects, fun facts, hobbies, etc.

Each YAML file contributes its top-level keys to the merged dict.
Templates access everything via the `portfolio` context variable, e.g.
  {{ portfolio.name }}, {{ portfolio.experience }}, {{ portfolio.projects }}
"""

import yaml
from pathlib import Path

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"


def load_portfolio() -> dict:
    data: dict = {}

    _merge_file(data, CONTENT_DIR / "profile.yaml")

    _merge_dir(data, CONTENT_DIR / "professional")
    _merge_dir(data, CONTENT_DIR / "personal")

    return data


def _merge_dir(data: dict, directory: Path) -> None:
    if not directory.exists():
        return
    for path in sorted(directory.glob("*.yaml")):
        _merge_file(data, path)


def _merge_file(data: dict, path: Path) -> None:
    if not path.exists():
        return
    with open(path, "r") as f:
        loaded = yaml.safe_load(f)
    if isinstance(loaded, dict):
        data.update(loaded)
