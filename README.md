# Vibe Listing

Listing photos in → a polished vertical listing video out. Just ask Claude Code.

| Say this | You get |
|---|---|
| "Make a listing video from these photos" + price, address, beds/baths | 9:16 Reel/TikTok/Short + 4:5 feed video: hook with price, address, feature callouts, stats, agent end card |
| (same request) | Listing description, social caption and hashtags to finish |
| "Make clips from this house tour / market update video" | Captioned vertical clips (`/clips`) |

Styles: **luxury** (dark + gold, serif titles, cinematic moves) or **modern** (bold, faster cuts).
Everything runs on your own computer. No API keys, no accounts.

## Install (in Claude Code)
```
/plugin marketplace add kadomius-AI/vibe-listing
/plugin install vibe-listing@vibe-listing
```
Needs macOS or Linux, Homebrew, Python 3.11–3.13 (set up automatically on first use).

## Built with (all free and open source, runs on your Mac)
| Job | Framework / model | License |
|---|---|---|
| Video in/out, cutting, loudness | FFmpeg, OpenCV | LGPL/GPL tool, Apache-2.0 |
| Face tracking | OpenCV YuNet | MIT |
| Transcription + word timing | Whisper (mlx-whisper on Apple Silicon) | MIT |
| Voiceover with word timing | Kokoro-82M | Apache-2.0 |
| Original music | ACE-Step | Apache-2.0 |
| Beat detection | librosa | ISC |
| Sound effects | synthesized in code (original) | — |
| Voice isolation | Demucs (htdemucs) | MIT |
| 3D parallax on photos | Depth Anything V2 Small (PyTorch + transformers) | Apache-2.0 |
| Product cut-outs | Segment Anything (SAM ViT-B) | Apache-2.0 |
| Person cut-outs / backgrounds | MediaPipe selfie segmenter | Apache-2.0 |
| Face edits (beard / stubble / shave, consent only) | SDXL Inpainting via diffusers + MediaPipe Face Landmarker | CreativeML Open RAIL++-M / Apache-2.0 |
| AI upscaling of old low-res footage | Real-ESRGAN x4 via spandrel | BSD-3 / MIT |
| Graphics and text | Pillow + NumPy | MIT-CMU / BSD |
| AI runtime | PyTorch (Apple GPU), MLX | BSD / MIT |
No API keys, no accounts, no payments. First use downloads about 10–15 GB of models once.

Fonts: Montserrat, Anton, Playfair Display, Inter — SIL Open Font License 1.1.
