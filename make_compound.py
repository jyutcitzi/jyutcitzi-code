from dict_imports import *

################################
# Change to either web or font in command:
# python make_compound.py web > jyutcitzi_web.compound.dict.yaml
# python make_compound.py font > jyutcitzi_font.compound.dict.yaml
import sys
mode = sys.argv[1]
#
################################
assert mode in ['font', 'web']

def add_repeats(src_arr, repeat_sym="[repeat]"):
    src_proc = copy.deepcopy(src_arr)
    for i in range(len(src_arr)-1):
        if src_arr[i] == src_arr[i+1]:
            src_proc[i+1] = repeat_sym
    return src_proc

replace_dict = {"coet1": "ceot1",
                "seo4": "soe4",
                "la3": "laa3",
                "la1": "laa1",
                "a1": "aa1",
                "sa4": "saa4",
                "ga3": "gaa3",
                "hng6": "hang6",
                "za1": "zaa1",
                "za3": "zaa3"}
start_line_idx = 22721

print("""# Rime dictionary
# encoding: utf-8

---
name: jyutcitzi_"""+mode+""".compound
version: "2"
sort: by_weight
use_preset_vocabulary: true
...
""")

vocab_dict = {}
font_vocab_dict = {}
with open("./rime/src/jyut6ping3.dict.yaml", 'r') as f:
     for i, line in enumerate(f.readlines(), 0):
          if i >= start_line_idx:
              raw_tokens = line[:-1].split("\t")
              assert len(raw_tokens) in [2, 3]
              if len(raw_tokens) == 3:
                  tgt, src, weight = raw_tokens
              elif len(raw_tokens) == 2:
                  tgt, src = raw_tokens
                  weight = ""

              # the original dictionary has a typo:
              if tgt == "送畀我都唔吼睺啦":
                  tgt = "送畀我都唔睺啦"

              src_tokens = src.split(" ")
              src_tokens = [replace_dict.get(tok, tok) for tok in src_tokens]
              src_arr = [x[:-1] for x in src_tokens]

              src_proc = add_repeats(src_arr)
              src_proc_w_pitch = add_repeats(src_tokens)

              src_with_pitch = "·".join([mapping[x] for x in src_proc_w_pitch]) + "·"
              src_wo_pitch = "·".join([mapping[x] for x in src_proc]) + "·"

              if len(weight) > 0:
                  try:
                      weight_more = str(float(weight) + 1)
                  except:
                      weight_more = weight
              else:
                  weight_more = weight
              # print(src_wo_pitch, " ".join(src_arr), weight_more, sep="\t")
              # print(src_with_pitch, " ".join(src_tokens), weight, sep="\t")

              final_weight = 100000.0
              if len(weight) > 0:
                  try:
                      final_weight += float(weight)
                  except:
                      pass

              # groupby tokens to get max weight
              # helps save memory
              src_token_string = "[SEP]" + " ".join(src_tokens)
              src_arr_string = "[SEP]" + " ".join(src_arr)
              pitch_key = src_with_pitch + src_token_string
              no_pitch_key = src_wo_pitch + src_arr_string
              try:
                  score = vocab_dict[pitch_key]
              except:
                  score = -1
              pitch_score = max(score, final_weight)
              vocab_dict[pitch_key] = pitch_score
              font_vocab_dict[pitch_key] = pitch_score

              try:
                  score = vocab_dict[no_pitch_key]
              except:
                  score = -1
              no_pitch_score = max(score, final_weight + 10.0)
              vocab_dict[no_pitch_key] = no_pitch_score
              font_vocab_dict[no_pitch_key] = no_pitch_score

              # form goigaakhonzi-derived compounds
              if has_goigaakhonzi(tgt):
                  tgt_font, tgt_web = tgt2webandfont(tgt, src)

                  tgtweb_pitch = tgt_web + src_token_string
                  tgtweb_no_pitch = tgt_web + src_arr_string
                  vocab_dict[tgtweb_pitch] = pitch_score
                  vocab_dict[tgtweb_no_pitch] = no_pitch_score

                  tgtfont_pitch = tgt_font + src_token_string
                  tgtfont_no_pitch = tgt_font + src_arr_string
                  font_vocab_dict[tgtfont_pitch] = pitch_score
                  font_vocab_dict[tgtfont_no_pitch] = no_pitch_score

# weight_str = str(weight)
weight_str = "0%"
if mode == "font":
    for outs_ins, weight in font_vocab_dict.items():
        outs, ins = outs_ins.split("[SEP]")
        outs_chars = "".join(
                [syl_pitch_to_char_pitch(x)
                for x in outs.split("·")[:-1]])
        print(outs_chars, ins, weight_str, sep="\t")
elif mode == 'web':
    for outs_ins, weight in vocab_dict.items():
        outs, ins = outs_ins.split("[SEP]")
        print(outs, ins, weight_str, sep="\t")
