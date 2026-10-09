cd /home/claude/work
python3 assemble.py > logs/asm.log 2>&1 && python3 gen_data.py > logs/gd.log 2>&1 || { echo FAIL_DATA; exit 1; }
python3 gen_standing.py; python3 gen_links.py; python3 gen_fav.py; python3 gen_docx.py
python3 add_mahdi_tools.py
python3 - <<'PY'
import json
p='/home/claude/work/build/tools/short_ids.json';s=json.load(open(p))
for k in range(275,288): s[str(k)]=''
s['184']='لجنة حقوق الطفل: هيئة الأمم المتحدة التي تفسر اتفاقية حقوق الطفل'
json.dump(s,open(p,'w'),ensure_ascii=False,indent=1)
PY
python3 gen_schedule.py
python3 simple.py ALL A /tmp/claude-0/sp/simA /tmp/claude-0/sp/simA/A.pdf || { echo FAIL_A; exit 1; }
python3 simple.py ALL B /tmp/claude-0/sp/simB /tmp/claude-0/sp/simB/B.pdf || { echo FAIL_B; exit 1; }
python3 pack_simple.py
sh runall.sh
echo REBUILD_DONE
