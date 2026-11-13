---
name: listing
description: >
  Turn real-estate listing photos (and optional clips) into a polished vertical listing video (9:16 Reels/TikTok/Shorts,
  plus 4:5 for feeds) with price, address, features and an agent end card, plus listing description and social captions.
  Use for "listing video", "just listed reel", "property video", "make a video for this house", "vibe listing".
---

# /listing — listing photos in, listing video + copy out

Run scripts through `../../scripts/run.sh` (auto-setup on first run). The user is not technical: do every step yourself.

## Steps
1. **Collect facts (one question at a time, only what's missing):** photos folder, price, address, beds/baths/sq ft,
   2–4 standout features, agent name, brokerage, phone, logo (optional), style (luxury or modern), status (Just Listed,
   Open House, Under Contract, Just Sold). Use only true facts. Never invent features or numbers.
2. **Look at the photos:** `run.sh listing.py inspect "<photos>" --out "<folder>"` → LOOK at `photos_sheet.jpg`.
   Choose the order: the single most impressive shot first (usually exterior hero or the view), then living → kitchen →
   primary suite → bath → outdoor/pool → twilight. Drop dark, blurry, duplicate or cluttered shots. 6–12 photos is ideal.
3. **Scaffold:** `run.sh listing.py scaffold --photos "a.jpg,b.jpg,…" --price "…" --address "…" --beds 4 --baths 3.5 --sqft 3200 --hook "…" --features "A|B|C" --agent "…" --brokerage "…" --phone "…" --style luxury --out "<folder>/listing"`
4. **Polish the plan** (`listing.json`): make the hook line specific (the one thing a buyer would remember), match each
   feature callout to the photo that shows it, keep text short.
5. **Render:** `run.sh listing.py render "<folder>/listing" --formats vertical,portrait` → LOOK at each `_sheet.png`;
   fix any text over important details, then re-render.
6. **Write the copy** in `listing_copy.md` (description, caption, hashtags) using only true facts, then deliver the videos + copy.

## Best practices (from top luxury and high-performing listing content)
- **Hook in 3 seconds:** best shot + status badge + price large and central + one-line hook. No logos or slow intros first.
- **Length:** 15–45 s for Reels/TikTok/Shorts. Every shot earns its place.
- **Pacing by price point:** luxury = slower, cinematic moves (~2.4 s/shot, gentle push-ins and pans, whole-room framing);
  mid-market/modern = quicker cuts (~1.8 s/shot).
- **Motion on every still:** push-in, pull-out or pan. Never a static slideshow.
- **Text system:** price big on the hook frame; address as a subtle lower third on the next shot; short feature
  callouts on the matching rooms; beds/baths/sq ft once; agent name, brokerage, phone and a soft CTA ("DM for a private tour") at the end.
- **Personality sells:** if the agent has a short intro or walkthrough clip, put it right after the hook (run it through `/clips` first).
- **Formats:** 9:16 for reach (Reels/TikTok/Shorts), 4:5 for the feed.
- **Music:** understated and licensed; use a platform's licensed library or a user-supplied track. Never imply a home has
  features it doesn't; show the property honestly.
- Keep any brokerage's brand and other agents' names out unless the user is that agent/brokerage.
