import json
import string
from pathlib import Path

import config

ALLOWED_NAME_CHARS = set(string.ascii_letters + string.digits + " _-")


def _score_path():
    return Path(__file__).with_name(config.SCOREBOARD_FILE)


def load_scores():
    path = _score_path()
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as file_handle:
            data = json.load(file_handle)
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(data, list):
        return []
    cleaned = []
    for entry in data:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        score = entry.get("score")
        if isinstance(name, str) and isinstance(score, int):
            cleaned.append({"name": name, "score": score})
    return cleaned


def save_scores(entries):
    path = _score_path()
    with path.open("w", encoding="utf-8") as file_handle:
        json.dump(entries, file_handle, indent=2)


def update_score(name, score):
    entries = load_scores()
    for entry in entries:
        if entry["name"] == name:
            entry["score"] = score
            save_scores(entries)
            return entries
    entries.append({"name": name, "score": score})
    save_scores(entries)
    return entries


def get_leaderboard():
    entries = load_scores()
    return sorted(entries, key=lambda item: (-item["score"], item["name"].lower()))


def validate_name(name):
    if not name:
        return "Name cannot be empty."
    if name != name.strip():
        return "Name cannot start or end with a space."
    if len(name) > config.NAME_MAX_LENGTH:
        return f"Name must be {config.NAME_MAX_LENGTH} characters or fewer."
    for char in name:
        if char not in ALLOWED_NAME_CHARS:
            return "Use letters, numbers, spaces, _ or - only."
    return None
