"""Download the exact transcript of the source video.

Usage:
    pip install youtube-transcript-api
    python scripts/get_transcript.py            # -> source/transcript.txt
    python scripts/get_transcript.py VIDEO_ID   # any other video

Falls back to yt-dlp auto-subs if youtube-transcript-api is unavailable:
    yt-dlp --skip-download --write-auto-subs --sub-langs en --sub-format vtt \
        -o source/transcript "https://www.youtube.com/watch?v=uSTGNHGFOAo"

The transcript is YouTube's auto-generated English track, so expect ASR
errors (e.g. "copyrightiting" for "copywriting", "Chelini" for "Cialdini").
source/video-notes.md is the cleaned, paraphrased study of it that the
skill was built from.
"""

import sys
from pathlib import Path

VIDEO_ID = "uSTGNHGFOAo"
OUT = Path(__file__).resolve().parent.parent / "source" / "transcript.txt"


def fmt(seconds: float) -> str:
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def main() -> None:
    video_id = sys.argv[1] if len(sys.argv) > 1 else VIDEO_ID
    from youtube_transcript_api import YouTubeTranscriptApi

    fetched = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
    lines = [f"[{fmt(snip.start)}] {snip.text}" for snip in fetched]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {len(lines)} lines to {OUT}")


if __name__ == "__main__":
    main()
