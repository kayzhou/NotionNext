#!/usr/bin/env bash
# 从矢量源导出站点所需的全部图标资源。
# 依赖: rsvg-convert (librsvg), ImageMagick
set -euo pipefail
cd "$(dirname "$0")"
PUB=../../public
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

python3 build_final.py

# favicon: 单字小印，16/32/48/64 四档（浏览器实际使用的尺寸）
for s in 16 32 48 64; do
  rsvg-convert -w $s -h $s final/seal-zhou-mark.svg -o "$TMP/mark-$s.png"
done
magick "$TMP/mark-16.png" "$TMP/mark-32.png" "$TMP/mark-48.png" "$TMP/mark-64.png" final/favicon.ico
cp final/favicon.ico "$PUB/favicon.ico"
magick "$TMP/mark-48.png" -strip "$PUB/favicon.png"
cp final/seal-zhou-mark.svg "$PUB/favicon.svg"

# iOS 主屏图标 180px
rsvg-convert -w 180 -h 180 final/seal-zhou-mark.svg -o "$TMP/mark-180.png"
magick "$TMP/mark-180.png" -strip "$PUB/apple-touch-icon.png"

# 头像：四字主印
rsvg-convert -w 512 -h 512 final/seal-zhouzhenkun.svg -o "$TMP/full-512.png"
magick "$TMP/full-512.png" -strip "$PUB/avatar.png"
cp final/seal-zhouzhenkun.svg "$PUB/avatar.svg"

# 品牌资源目录
mkdir -p "$PUB/brand/seal"
for f in seal-zhouzhenkun seal-zhou-mark seal-zhouzhenkun-ink seal-zhouzhenkun-transparent lockup-horizontal; do
  cp "final/$f.svg" "$PUB/brand/seal/$f.svg"
done
magick "$TMP/full-512.png" -strip "$PUB/brand/seal/seal-512.png"
rsvg-convert -w 1024 final/seal-zhouzhenkun.svg -o "$TMP/s1024.png"
magick "$TMP/s1024.png" -strip "$PUB/brand/seal/seal-zhouzhenkun-1024.png"
rsvg-convert -w 1024 final/lockup-horizontal.svg -o "$TMP/l1024.png"
magick "$TMP/l1024.png" -strip "$PUB/brand/seal/lockup-horizontal-1024.png"

echo "导出完成 -> $PUB"
