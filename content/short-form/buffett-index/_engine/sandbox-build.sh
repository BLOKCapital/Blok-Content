#!/bin/bash
# Runs in the Higgsfield sandbox (this repo's container can't reach the image/voice hosts).
# Usage: sandbox-build.sh <root>   (root = content/short-form/buffett-index inside a checkout, with raw/*.png and vo/<slug>/vo.{m4a,json})
set -e
ROOT=$1; cd $ROOT
mkdir -p img
for f in raw/*.png; do n=$(basename $f .png); [ -f img/$n.png ] && continue
  python3 _engine/cutout.py $f /tmp/$n-cut.png ${TOL:-22} >/dev/null
  python3 _engine/halftone.py /tmp/$n-cut.png img/$n.png ${CELL:-7} 22 1.35 >/dev/null; echo img/$n.png; done
cp -n _engine/fonts/* _engine/fonts/ 2>/dev/null || true
for s in bogles-folly buttonwood-tree know-nothing-investor one-customer; do
  cp vo/$s/vo.json $s/build/vo.json; cp vo/$s/vo.m4a $s/build/vo.m4a
  python3 _engine/build-timeline.py $s/build/script.txt $s/build/vo.json $s/build/timeline.js | tail -1
done
