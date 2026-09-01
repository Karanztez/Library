#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
RAW = "https://raw.githubusercontent.com/Karanztez/Library/main/"
SKIP = {".git", ".github", "scripts"}

LABELS = {
    "PNG (Transparent)": "โปร่งใส",
    "PNG (Black background)": "พื้นดำ",
    "Default": "ต้นฉบับ",
    "Inverted": "กลับสี",
    "Transparent": "โปร่ง",
    "Unity samples": "ตัวอย่าง",
}

EXTS = {".png", ".webp", ".gif", ".jpg", ".jpeg"}


def label_for(folder: str) -> str:
    return LABELS.get(folder, folder)


def main() -> None:
    grouped: dict[str, list[dict]] = {}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in EXTS:
            continue
        if any(part in SKIP or part.startswith(".") for part in path.parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        folder = rel.split("/", 1)[0] if "/" in rel else "คลัง"
        group = label_for(folder)
        name = path.stem
        grouped.setdefault(group, []).append(
            {
                "id": rel.replace(" ", "_"),
                "label": name,
                "path": rel,
                "url": RAW + quote(rel),
                "tint": "#ffffff",
            }
        )
    catalog = {
        "updated": __import__("datetime").datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "groups": [
            {"id": label, "label": label, "items": items}
            for label, items in grouped.items()
        ],
        "count": sum(len(v) for v in grouped.values()),
    }
    (ROOT / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote catalog.json ({catalog['count']} files, {len(grouped)} groups)")


if __name__ == "__main__":
    main()
