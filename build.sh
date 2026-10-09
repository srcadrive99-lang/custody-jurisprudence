#!/bin/sh
# Rebuild every product with one command:  ./build.sh   (needs python3, playwright+chromium, segno, jsonschema, pymupdf optional)
set -e
ROOT=$(cd "$(dirname "$0")" && pwd)
W="$ROOT/_work"
rm -rf "$W"; mkdir -p "$W/out" "$W/build" "$W/verify" "$W/logs"
cp "$ROOT"/scripts/* "$W"/
cp "$ROOT"/data/new_cards.json "$ROOT"/data/links_fix.json "$ROOT"/data/id_map.json "$ROOT"/data/base_v1_15.json "$W"/
cp "$ROOT"/base/* "$W/out/"
cp "$ROOT"/verify/* "$W/verify/"
mkdir -p "$W/build/tools"; cp "$ROOT"/tools/* "$W/build/tools/"
cp "$ROOT"/data/nuqul_7_9.schema.json "$W/out/" 
for f in "$W"/*.py; do sed -i "s#/home/claude/work#$W#g; s#/mnt/user-data/outputs/nuqul_7_9.schema.json#$W/out/nuqul_7_9.schema.json#g" "$f"; done
cd "$W"
python3 assemble.py
python3 gen_data.py
python3 gen_standing.py; python3 gen_links.py; python3 gen_fav.py; python3 gen_docx.py
python3 render1.py "$W/build/NUQUL_7_9_CARDS_MOBILE.html" m "$W/build/NUQUL_7_9_CARDS_MOBILE.pdf"
python3 render1.py "$W/build/NUQUL_7_9_CARDS.html" w "$W/build/NUQUL_7_9_CARDS.pdf"
python3 shots.py; python3 fb.py ""; python3 pack_fb.py
mkdir -p "$W/build/simple_A" "$W/build/simple_B"
python3 simple.py ALL A "$W/build/simple_A" "$W/build/simple_A/A.pdf"
python3 simple.py ALL B "$W/build/simple_B" "$W/build/simple_B/B.pdf"
python3 gen_schedule.py
echo "Done: products in $W/build"
