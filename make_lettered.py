from dict_imports import *

################################
# Change to either core, web or font
# python make_lettered.py core > jyutcitzi_core.lettered.dict.yaml
# python make_lettered.py web > jyutcitzi_web.lettered.dict.yaml
# python make_lettered.py font > jyutcitzi_font.lettered.dict.yaml
import sys
mode = sys.argv[1]
#
################################
assert mode in ['core', 'font', 'web']

print("""# Rime dictionary
# encoding: utf-8

---
name: jyutcitzi_"""+mode+""".lettered
version: "2"
sort: by_weight
use_preset_vocabulary: true
...""")

start_line_idx = 32
with open("./rime/src/jyut6ping3.lettered.dict.yaml", 'r') as f:
     for i, line in enumerate(f.readlines(), 0):
          if i >= start_line_idx:
              tgt, src = line[:-1].split("\t")
              if "feel" in src:
                  continue
              src = src.replace("oet","eot") \
                        .replace("sa4","saa4")
              src_arr = [x[:-1] for x in src.split(" ")]

              src_proc = copy.deepcopy(src_arr)
              for i in range(len(src_arr)-1):
                  if src_arr[i] == src_arr[i+1]:
                      src_proc[i+1] = "[repeat]"

              src_proc_w_pitch = src.split(" ")
              for i in range(len(src_arr)-1):
                  if src_proc_w_pitch[i] == src_proc_w_pitch[i+1]:
                      src_proc_w_pitch[i+1] = "[repeat]"

              jcztgt_with_pitch = "·".join([mapping[x] for x in src_proc_w_pitch]) + "·"
              jcztgt_wo_pitch = "·".join([mapping[x] for x in src_proc]) + "·"
              src_wo_pitch = " ".join(src_arr)

              # tgt_has_rep = has_repetition(tgt)
              # if tgt_has_rep
              #     tgt_wo_rep = remove_repetition(tgt)

              # TODO: deal with repetition
              if mode == 'web':
                  # JCZ-only
                  print(jcztgt_with_pitch, src, sep="\t")
                  print(jcztgt_wo_pitch, src_wo_pitch, sep="\t")
              elif mode == 'core':
                  # original one
                  print(tgt, src, sep='\t')
                  print(tgt, src_wo_pitch, sep='\t')
                  # print repetition-free lettered compund

              if mode == 'font':
                  jcztpwp_char = [syl_pitch_to_char_pitch(x) for x in jcztgt_with_pitch[:-1].split("·")]
                  jcztp_char = [syl_pitch_to_char_pitch(x) for x in jcztgt_wo_pitch[:-1].split("·")]
                  jcztgt_with_pitch_chars = "".join(jcztpwp_char)
                  jcztgt_wo_pitch_chars = "".join(jcztp_char)
                  print(jcztgt_with_pitch_chars, src, sep="\t")
                  print(jcztgt_wo_pitch_chars, src, sep="\t")

              shd_change = any(c.encode('utf-8').isalpha() for c in tgt) and \
                           not all(c.encode('utf-8').isalnum() or c == '-' for c in tgt)
              if has_goigaakhonzi(tgt) or shd_change:
                  tgt_font, tgt_web = tgt2webandfont(tgt, src)
                  if mode == 'web':
                      print(tgt_web, src, sep='\t')
                      # print(tgt_web, src_wo_pitch, sep='\t')
                  elif mode == 'font':
                      print(tgt_font, src, sep='\t')
                      # print(tgt_font, src_wo_pitch, sep='\t')
