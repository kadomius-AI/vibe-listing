"""End-to-end listing render from generated photos (no voice/music, so it runs offline and fast)."""
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def _photos(d, n=4):
    out = []
    for i in range(n):
        img = np.zeros((900, 1350, 3), np.uint8)
        img[:] = (40 + 40 * i, 90, 160 - 20 * i)
        cv2.rectangle(img, (200, 300), (1100, 800), (200, 200, 210), -1)        # "house"
        cv2.rectangle(img, (500, 550), (650, 800), (60, 60, 70), -1)             # "door"
        p = d / f"p{i}.jpg"
        cv2.imwrite(str(p), img)
        out.append(str(p))
    return ",".join(out)


def test_listing_scaffold_and_render(tmp_path):
    photos = _photos(tmp_path)
    od = tmp_path / "listing"
    r = subprocess.run([sys.executable, str(SCRIPTS / "listing.py"), "scaffold", "--photos", photos, "--price", "$500,000",
                        "--address", "1 Test St, Testville NJ", "--beds", "3", "--baths", "2", "--style", "modern",
                        "--no-voice", "--no-music", "--out", str(od)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-2000:]
    spec = json.loads((od / "listing.json").read_text())
    for sc in spec["scenes"]:                          # cheap test: plain moves instead of depth parallax
        if str(sc.get("motion", "")).startswith("parallax"):
            sc["motion"] = "zoom_in"
    (od / "listing.json").write_text(json.dumps(spec))
    r = subprocess.run([sys.executable, str(SCRIPTS / "listing.py"), "render", str(od)], capture_output=True, text=True)
    qa = json.loads((od / "listing_vertical.mp4.qa.json").read_text())
    for k in ("render", "dimensions", "fps", "black", "audio"):
        assert qa["checks"][k]["ok"], (k, qa["checks"][k], r.stderr[-1500:])
