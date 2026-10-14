#!/usr/bin/env bash
# Download the 5 CC0 background photos from Wikimedia Commons and crop them to 1080x1440 (centre crop).
#   bash fetch-photos.sh <outDir>
set -euo pipefail
OUT=$1; mkdir -p "$OUT"
declare -A F=(
  [hook]="United_Daily_News_reader_at_Louisa_Coffee_Minsheng_Fujin_Store_(42287881175).jpg"
  [myth1]="Financial_Risk_Dice_On_Newspaper.jpg"
  [myth2]="Coffee-desk-laptop-notebook_(24244320481).jpg"
  [myth3]="Apple-iphone-desk-laptop_(23699175703).jpg"
  [cta]="Woman_using_smartphone.jpeg"
)
for k in hook myth1 myth2 myth3 cta; do
  curl -sfL -A "BLOK-Content/1.0 (sn@blokcapital.io)" "https://commons.wikimedia.org/wiki/Special:FilePath/${F[$k]}?width=2000" -o "$OUT/$k.src.jpg"
  ffmpeg -y -loglevel error -i "$OUT/$k.src.jpg" -vf "scale=1080:1440:force_original_aspect_ratio=increase,crop=1080:1440" -q:v 2 "$OUT/$k.jpg"
  echo "$k ok"
done
