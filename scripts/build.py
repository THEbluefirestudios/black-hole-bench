"""Build the Pages gallery without rewriting model-generated HTML."""
import json
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"


def build():
    entries = []
    for path in sorted((ROOT / "submissions").rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Submission symlinks are unsupported: {path}")
        if not path.is_file() or path.suffix.lower() not in {".html", ".htm"}:
            continue
        relative = path.relative_to(ROOT)
        if len(relative.parts) < 3:
            raise ValueError(f"Put {relative} inside submissions/<model-name>/")
        metadata_path = path.with_suffix(".json")
        metadata = json.loads(metadata_path.read_text()) if metadata_path.exists() else {}
        if not isinstance(metadata, dict):
            raise ValueError(f"Expected an object in {metadata_path}")
        for key in ("model", "date", "notes"):
            if key in metadata and not isinstance(metadata[key], str):
                raise ValueError(f"{key} must be text in {metadata_path}")
        entries.append({
            "model": metadata.get("model", relative.parts[1]),
            "run": path.stem,
            "date": metadata.get("date", ""),
            "notes": metadata.get("notes", ""),
            "url": quote(relative.as_posix(), safe="/"),
        })
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "site", OUT)
    shutil.copytree(ROOT / "submissions", OUT / "submissions", ignore=shutil.ignore_patterns(".gitkeep"))
    shutil.copy2(ROOT / "PROMPT.txt", OUT / "PROMPT.txt")
    (OUT / "catalog.json").write_text(json.dumps(entries, indent=2) + "\n")
    (OUT / ".nojekyll").touch()
    print(f"Built {len(entries)} submissions in {OUT}")


if __name__ == "__main__":
    build()
