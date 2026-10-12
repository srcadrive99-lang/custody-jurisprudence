cd /home/claude/work
python3 assemble.py > logs/asm.log 2>&1 && python3 gen_data.py > logs/gd.log 2>&1 || { echo FAIL_DATA; exit 1; }
python3 gen_standing.py; python3 gen_links.py; python3 gen_fav.py; python3 gen_docx.py
python3 add_mahdi_tools.py
python3 add_azhar_tools.py
python3 add_hujaj_tools.py
python3 add_harm2_tools.py
python3 add_v125_tools.py
python3 add_v126_tools.py
python3 add_v127_tools.py
python3 add_v128_tools.py
python3 add_v129_tools.py
python3 add_v130_tools.py
python3 gen_schedule.py
python3 simple.py ALL A /tmp/claude-0/sp/simA /tmp/claude-0/sp/simA/A.pdf || { echo FAIL_A; exit 1; }
python3 simple.py ALL B /tmp/claude-0/sp/simB /tmp/claude-0/sp/simB/B.pdf || { echo FAIL_B; exit 1; }
REVIEW=1 python3 simple.py ALL A /tmp/claude-0/sp/rev /tmp/claude-0/sp/rev/R.pdf || { echo FAIL_REV; exit 1; }
R=/mnt/user-data/outputs/بطاقات_للمراجعة; rm -rf $R; mkdir -p $R; cp /tmp/claude-0/sp/rev/R.pdf $R/بطاقات_للمراجعة.pdf; (cd /tmp/claude-0/sp/rev/img_A && zip -q -j $R/صور_بطاقات_للمراجعة.zip *.png)
rm -f /mnt/user-data/outputs/البطاقات_المختصرة/صور_نمط_*.zip; python3 pack_simple.py
sh runall.sh
echo REBUILD_DONE
