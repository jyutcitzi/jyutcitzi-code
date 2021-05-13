from dict_imports import *

################################
# Change to either web or font
# python make_phrase.py web > jyutcitzi_web.phrase.dict.yaml
# python make_phrase.py font > jyutcitzi_font.phrase.dict.yaml
import sys
mode = sys.argv[1]
#
################################
assert mode in ['font', 'web']

print("""# Rime dictionary
# encoding: utf-8

---
name: jyutcitzi_"""+mode+""".phrase
version: "1"
sort: by_weight
use_preset_vocabulary: true
...
""")
start_line_idx = 28
phrase_set = set()
with open("./rime/src/jyut6ping3.phrase.dict.yaml", 'r') as f:
    for i, line in enumerate(f.readlines(), 0):
        if i >= start_line_idx:
            tgt = line[:-1]
            if has_goigaakhonzi(tgt):
                 tgt_font, tgt_web = tgt2webandfont(tgt, "")
                 if mode == 'font':
                     phrase_set.add(tgt_font)
                 elif mode == 'web':
                     phrase_set.add(tgt_web)
for phrase in sorted(list(phrase_set)):
    print(phrase)
