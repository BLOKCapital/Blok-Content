#!/usr/bin/env bash
# Downloads the local voice (Kokoro) and speech-recognition (Whisper small.en via sherpa-onnx) models.
# Both come from GitHub releases, which this machine can reach. Usage: bash scripts/qa/setup-models.sh [dir]
set -euo pipefail
D="${1:-$HOME/.cache/blok-models}"; mkdir -p "$D"; cd "$D"
pip install -q kokoro-onnx soundfile sherpa-onnx pyspellchecker
[ -f kokoro-v1.0.onnx ] || curl -sSLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -f voices-v1.0.bin ] || curl -sSLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
[ -d sherpa-onnx-whisper-small.en ] || curl -sSL https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.en.tar.bz2 | tar xj
echo "models in $D"
