#!/usr/bin/env bash
# One-time setup for the video reference library (free, CPU only).
# Installs yt-dlp + sherpa-onnx and fetches the local whisper small.en model used for transcripts.
set -euo pipefail
pip install -q --upgrade yt-dlp sherpa-onnx numpy pillow
M="$HOME/.cache/blok-models/sherpa-onnx-whisper-small.en"
mkdir -p "$M"
for f in small.en-encoder.int8.onnx small.en-decoder.int8.onnx small.en-tokens.txt; do
  [ -s "$M/$f" ] || curl -sSL -o "$M/$f" "https://huggingface.co/csukuangfj/sherpa-onnx-whisper-small.en/resolve/main/$f"
done
command -v ffmpeg >/dev/null || echo "ffmpeg is missing: install it (apt-get install ffmpeg / brew install ffmpeg)"
echo "video-refs ready: python3 scripts/video-refs/vref.py --help"
