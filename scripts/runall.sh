#!/bin/sh
cd /home/claude/work
python3 render1.py /home/claude/work/build/NUQUL_7_9_CARDS_MOBILE.html m /home/claude/work/build/NUQUL_7_9_CARDS_MOBILE.pdf > logs/pdf_m.log 2>&1
python3 render1.py /home/claude/work/build/NUQUL_7_9_CARDS.html w /home/claude/work/build/NUQUL_7_9_CARDS.pdf > logs/pdf_w.log 2>&1
python3 shots.py > logs/shots.log 2>&1
python3 fb.py "" > logs/fb.log 2>&1
python3 fb_cover.py >> logs/fb.log 2>&1
python3 pack_fb.py >> logs/fb.log 2>&1
echo ALLDONE >> logs/fb.log
