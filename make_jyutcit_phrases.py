from dict_imports import *
# python make_jyutcit_phrases.py > jyutcitzi.jyutcit_phrases.dict.yaml

################################
# Change to either web or font
# python make_jyutcit_phrases.py web > jyutcitzi_web.jyutcit_phrases.dict.yaml
# python make_jyutcit_phrases.py font > jyutcitzi_font.jyutcit_phrases.dict.yaml
import sys
mode = sys.argv[1]
#
################################
assert mode in ['font', 'web']

print("""# Rime dictionary
# encoding: utf-8

---
name: jyutcitzi.jyutcit_phrases
version: "2"
sort: by_weight
use_preset_vocabulary: true
...""")

def split_outs(outs):
    outs_split = outs
    for dot in ["·","．"]:
        if dot in outs:
            outs_split = outs_split.split(dot)
    return outs_split
def temp_mapping(input):

    if len(input) == 1:
        return input
    elif input in hex_dict:
        return hex_dict[input]
    elif input[1:] in hex_dict:
        return input[0] + hex_dict[input[1:]]
    elif input[:-1] in hex_dict:
        return hex_dict[input[:-1]] + input[-1]
    else:
        return input
def outs_to_new_out(outs):
    if mode == 'font':
        outs_split = split_outs(outs)
        if outs_split[-1] == "":
            outs_split = outs_split[:-1]
        new_out = "".join([temp_mapping(syl) for syl in outs_split])
        return new_out
        out_dict[new_out] = (ins, "100000.0")
    else:
        return outs


with open("./rime/custom_list.txt") as file:
    out_dict = {}
    for line in file.readlines():
        outs, ins = line[:-1].split("\t") # -1 to remove newline
        out_dict[outs_to_new_out(outs)] = (ins, "100000.0")

        # check to contain pitch
        pitches = "¯´⁼˝ﾞ\'\"" # everything but "`", since that can be used in cons/vow-only glyhs
        outx = ""
        for out in outs:
            frag = ''.join(c for c in out if c not in pitches)
            outx += frag
        outx = outx.replace('``','`')
        out_dict[outs_to_new_out(outx)] = (ins, "100000.0")

    for formatted_out in out_dict:
        ins, score = out_dict[formatted_out]
        print(formatted_out, ins, score, sep="\t")
