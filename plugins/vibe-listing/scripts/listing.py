#!/usr/bin/env python3
"""/listing — listing photos in, a luxury vertical listing video (+ copy) out.

  listing.py inspect PHOTOS_DIR --out DIR
      Numbered contact sheet of every photo (with size/orientation/brightness) so Claude can pick the order:
      hero exterior first, then the best rooms, then outdoor/twilight.

  listing.py scaffold --photos "DIR or a.jpg,b.jpg,..." --price "$1,250,000" --address "12 Ocean Ave, Rumson NJ"
                      --beds 4 --baths 3.5 [--sqft 3200] [--hook "Waterfront modern with a private dock"]
                      [--features "Chef's kitchen|Heated pool|Primary suite with terrace"]
                      [--agent "Name"] [--brokerage "Company"] [--phone "..."] [--logo logo.png]
                      [--style luxury|modern] [--status "JUST LISTED"] [--cta "DM for a private tour"]
                      [--music track.mp3] --out DIR
      Writes listing.json (the video plan) + listing_copy.md (description and social captions to finish).

  listing.py render DIR [--formats vertical,portrait]
      Renders listing_vertical.mp4 (9:16, Reels/TikTok/Shorts) and optionally listing_portrait.mp4 (4:5, feed).
"""
import argparse, json, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cv2
import numpy as np
from vibekit.motion import render_spec
from vibekit import qa

IMG = {".jpg", ".jpeg", ".png", ".webp", ".heic"}
STYLES = {
    # luxury: dark, gold, serif titles, slower moves
    "luxury": {"bg": "#0D0C0B", "accent": "#D4B67A", "text": "#FFFFFF", "cta_text": "#0D0C0B", "secs": 2.4},
    # modern: bright, bold sans, faster cuts
    "modern": {"bg": "#111111", "accent": "#FFFFFF", "text": "#FFFFFF", "cta_text": "#111111", "secs": 1.8},
}
MOTIONS = ["parallax_push", "parallax_right", "parallax_pull", "parallax_left", "parallax_up"]


def _photos(arg):
    p = Path(arg).expanduser()
    if p.is_dir():
        return sorted(f for f in p.iterdir() if f.suffix.lower() in IMG)
    return [Path(x).expanduser() for x in arg.split(",") if x.strip()]


def inspect(photos, out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    tiles, info = [], []
    for i, f in enumerate(_photos(photos), 1):
        im = cv2.imread(str(f))
        if im is None:
            continue
        h, w = im.shape[:2]
        br = float(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).mean())
        info.append({"n": i, "file": str(f), "size": [w, h], "orientation": "wide" if w > h * 1.1 else "tall" if h > w * 1.1 else "square",
                     "brightness": round(br)})
        t = cv2.resize(im, (360, int(360 * h / w)))
        t = cv2.copyMakeBorder(t, 0, max(0, 270 - t.shape[0]), 0, 0, cv2.BORDER_CONSTANT)[:270]
        cv2.putText(t, f"#{i}", (10, 34), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 0), 5)
        cv2.putText(t, f"#{i}", (10, 34), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2)
        tiles.append(t)
    rows = [np.hstack(tiles[i:i + 5] + [np.zeros_like(tiles[0])] * (5 - len(tiles[i:i + 5]))) for i in range(0, len(tiles), 5)]
    cv2.imwrite(str(out / "photos_sheet.jpg"), np.vstack(rows))
    return {"sheet": str(out / "photos_sheet.jpg"), "photos": info}


def _t(text, style, at=0.0, **kw):
    d = {"text": text, "style": style, "at": at}
    d.update(kw)
    return d


def scaffold(a):
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    st = STYLES[a.style]
    photos = []
    for i, f in enumerate(_photos(a.photos), 1):
        dst = out / f"photo_{i:02d}{f.suffix.lower()}"
        shutil.copy2(f, dst)
        photos.append(dst.name)
    if not photos:
        raise SystemExit("No photos found.")
    lux = a.style == "luxury"
    title_style = "title" if lux else "hook"
    stats = " · ".join(x for x in [f"{a.beds} BD" if a.beds else "", f"{a.baths} BA" if a.baths else "",
                                   f"{a.sqft} SQ FT" if a.sqft else ""] if x)
    feats = [f for f in (a.features or "").split("|") if f]
    secs = st["secs"]

    def wide(name):
        im = cv2.imread(str(out / name))
        return im is not None and im.shape[1] > im.shape[0] * 1.25

    scenes = []
    # 1) HOOK (first 3 s): hero photo, status badge, price big and central, one-line hook
    scenes.append({"type": "image", "src": photos[0], "duration": 3.0, "motion": "parallax_push", "transition": "cut",
                   "texts": [_t(a.status, "badge", 0.0, y=0.12),
                             _t(a.price, "price", 0.25, y=0.42),
                             *([_t(a.hook, "caption", 0.8, y=0.56)] if a.hook else [])]})
    # 2) address as a subtle lower third on the next shot
    rest = photos[1:]
    if rest:
        scenes.append({"type": "image", "src": rest[0], "duration": secs, "motion": "parallax_left",
                       "texts": [_t(a.address, "lower", 0.2, align="left", y=0.12)]})
        rest = rest[1:]
    # 3) feature callouts on the strongest rooms, then the remaining photos as clean beats
    for i, ph in enumerate(rest):
        sc = {"type": "image", "src": ph, "duration": secs, "motion": MOTIONS[i % len(MOTIONS)]}
        if i < len(feats):
            sc["texts"] = [_t(feats[i], "small" if lux else "badge", 0.25, y=0.20 if lux else 0.14)]
        scenes.append(sc)
    # 4) stats card
    if stats:
        scenes.append({"type": "image", "src": photos[0], "duration": 2.2, "motion": "parallax_pull",
                       "texts": [_t(stats, "small" if lux else "badge", 0.1, y=0.20 if lux else 0.14)]})
    # 5) agent end card + CTA
    end = [_t(a.agent or "Your Name", title_style, 0.0, y=0.42, anim="words")]
    if a.brokerage:
        end.append(_t(a.brokerage, "small", 0.15, y=0.50))
    if a.phone:
        end.append(_t(a.phone, "small", 0.25, y=0.55))
    end.append(_t(a.cta, "cta", 0.4, y=0.72))
    card = {"type": "card", "duration": 3.0, "bg": st["bg"], "texts": end}
    if a.logo:
        shutil.copy2(a.logo, out / ("logo" + Path(a.logo).suffix.lower()))
        card["logo"] = "logo" + Path(a.logo).suffix.lower()
    scenes.append(card)

    spec = {"style": a.style, "size": [1080, 1920], "fps": 30,
            "brand": {k: st[k] for k in ("bg", "accent", "text", "cta_text")}, "scenes": scenes,
            "transition": "fade" if lux else "auto", "sfx": True,
            "caption_style": "clean" if lux else "bold", "caption_y": 0.80}
    if lux:  # luxury alternates soft fades and zooms
        for k, sc in enumerate(scenes[1:], 1):
            sc.setdefault("transition", "zoom" if k % 2 else "fade")
    if not a.no_voice:
        beds = f"{a.beds} bedrooms" if a.beds else ""
        baths = f"{a.baths} baths" if a.baths else ""
        script = ". ".join(x for x in [a.status.title(), a.address, ", ".join(x for x in (beds, baths) if x),
                                         ", ".join(feats), a.hook or "", f"{a.cta}" + (f" with {a.agent}" if a.agent else "")] if x) + "."
        spec["voiceover"] = {"text": script, "voice": a.voice or ("warm_female" if lux else "confident_male"), "speed": 1.0}
    if a.music:
        shutil.copy2(a.music, out / ("music" + Path(a.music).suffix.lower()))
        spec["music"] = "music" + Path(a.music).suffix.lower()
    elif not a.no_music:
        spec["music"] = {"prompt": a.music_prompt or (
            "cinematic luxury ambient, warm piano, soft strings, slow elegant groove, 92 bpm, instrumental" if lux else
            "modern deep house, punchy kick, warm synth chords, uplifting, 120 bpm, instrumental"), "seed": 5, "seconds": 40}
    (out / "listing.json").write_text(json.dumps(spec, indent=1))
    total = sum(s["duration"] for s in scenes)
    copy = f"""# Listing copy — {a.address}

## MLS / website description (write 120–200 words, specific and true)
<Open with the single best thing about the home ({a.hook or 'the hook'}). Then flow: arrival/exterior → main living →
kitchen → primary suite → outdoor → location. Use real features only: {', '.join(feats) or 'list features'}.
{stats}. End with an invitation to tour.>

## Instagram / TikTok caption
{a.status.title()} · {a.address}
{a.hook or ''}
{stats} · {a.price}
{a.cta} → {a.agent or ''} {a.phone or ''}

## Hashtags (5–8, local + property type)
#<town>realestate #<county>homes #justlisted #luxuryhomes #newjersey
"""
    (out / "listing_copy.md").write_text(copy)
    return {"spec": str(out / "listing.json"), "copy": str(out / "listing_copy.md"), "scenes": len(scenes),
            "seconds": round(total, 1)}


def render(d, formats):
    d = Path(d)
    spec = json.loads((d / "listing.json").read_text())
    res = []
    for fmt in formats:
        s = dict(spec)
        s["size"] = {"vertical": [1080, 1920], "portrait": [1080, 1350]}[fmt]
        p = d / f"_spec_{fmt}.json"
        p.write_text(json.dumps(s))
        out = d / f"listing_{fmt}.mp4"
        render_spec(p, out)
        p.unlink()
        from vibekit import checks
        rep = checks.run(out, fmt=fmt)
        checks.save(rep, str(out) + ".qa.json")
        r = qa.report(out)
        r["qa"] = checks.summary(rep)
        r["passed"] = rep["passed"]
        res.append(r)
    return res


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("inspect"); i.add_argument("photos"); i.add_argument("--out", required=True)
    s = sub.add_parser("scaffold")
    for k in ("--photos", "--price", "--address", "--out"):
        s.add_argument(k, required=True)
    for k in ("--beds", "--baths", "--sqft", "--hook", "--features", "--agent", "--brokerage", "--phone", "--logo", "--music"):
        s.add_argument(k)
    s.add_argument("--style", default="luxury", choices=list(STYLES))
    s.add_argument("--status", default="JUST LISTED"); s.add_argument("--cta", default="DM for a private tour")
    s.add_argument("--voice"); s.add_argument("--music-prompt")
    s.add_argument("--no-voice", action="store_true"); s.add_argument("--no-music", action="store_true")
    r = sub.add_parser("render"); r.add_argument("dir"); r.add_argument("--formats", default="vertical")
    a = ap.parse_args()
    if a.cmd == "inspect":
        print(json.dumps(inspect(a.photos, a.out), indent=1))
    elif a.cmd == "scaffold":
        print(json.dumps(scaffold(a), indent=1))
    else:
        res = render(a.dir, a.formats.split(","))
        print(json.dumps(res, indent=1))
        if not all(r.get("passed", True) for r in res):
            sys.exit(2)


if __name__ == "__main__":
    main()
