#!/usr/bin/env bash
# One-time setup for the Brooks voice (free, local, CPU). Needs huggingface.co + PyPI + download.pytorch.org.
# Usage: bash setup.sh [venv_dir]
set -euo pipefail
VENV="${1:-$HOME/.cache/blok-voice/cb}"
python3 -m venv "$VENV"; . "$VENV/bin/activate"
pip install -q --upgrade pip
pip install -q torch torchaudio --index-url https://download.pytorch.org/whl/cpu
# --no-deps: chatterbox pins torch==2.6.0 and would pull ~3GB of CUDA wheels. CPU torch works fine.
pip install -q --no-deps chatterbox-tts
pip install -q "numpy>=2" librosa==0.11.0 s3tokenizer transformers==5.2.0 diffusers==0.29.0 resemble-perth \
  conformer==0.3.2 "safetensors>=0.5.3" pyloudnorm omegaconf soundfile
python -c "from chatterbox.tts import ChatterboxTTS; ChatterboxTTS.from_pretrained(device='cpu'); print('Brooks voice ready')"
echo "activate with: . $VENV/bin/activate"
