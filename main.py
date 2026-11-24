"""News-image entry: decode the front-page image beside this file to the output dir.

The image is stored as base64 split across entry.png.b64.0 and entry.png.b64.1
(because a single file is too large to push in one API call).

Run locally with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
The grader runs it with /output as the output dir and no network.
"""
import base64
import os
from pathlib import Path

here = Path(__file__).resolve().parent
out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
out_dir.mkdir(parents=True, exist_ok=True)
parts = []
for name in ("entry.png.b64.0", "entry.png.b64.1"):
    path = here / name
    if not path.exists():
        raise SystemExit(f"missing part {name}: the entry image is incomplete")
    parts.append(path.read_text().strip())
data = base64.b64decode("".join(parts))
if not data.startswith(b"\x89PNG\r\n\x1a\n"):
    raise SystemExit("decoded image is not a PNG: the base64 parts may be corrupted")
(out_dir / "entry.png").write_bytes(data)
print(f"wrote {out_dir / 'entry.png'} ({len(data)} bytes)")
