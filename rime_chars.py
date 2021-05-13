# TODO:
# leaving double vowels out for now
# add # character (do this by changing encode in lang file)

# command for generating font file (in UTF-16)
# e.g. python rime_chars.py > jyutcitzi_web.dict.yaml

from font.chars import *
from font.chars_vowel import vEnd_c_iterator, \
                             vEnd_cc_iterator, \
                             vs_c_iterator, \
                             vs_cc_iterator
import itertools
from collections import OrderedDict

# construct chars to hex dictionary
hex_dict = get_hex_dict("./font/fonts/mapping.txt", ng_tilde=True)

ngs_chars = [("ng",hex_dict["五`"]),
            ("m",hex_dict["五."])]

# make pitches optional
pitches_opt = [('','')] + pitches_only #
no_pitch = [('','')]

ng_cons = [(ng[0]+pitch[0], ng[1]+pitch[1]) \
            for ng, pitch in itertools.product(ngs, pitches_opt)]

gen_cons = consonants + r_only + many_cons_opt_pitch + many_cons_no_pitch
# ---------------
# NO "S"
#(C|many C)Vp
cons_vow = [(cons[0]+vowel[0]+pitch[0],
             cons[1]+vowel[1]+pitch[1]) \
                    for cons, vowel, pitch in \
                    itertools.product(gen_cons, vowels, pitches_opt)]

#Vp
vow = [(vowel[0]+pitch[0], vowel[1]+'`'+pitch[1]) \
                    for vowel, pitch in \
                    itertools.product(vowels, pitches_opt)]
#(C|many C)[Vow]p.[Sup]
cons_vs = [(cons[0]+vs[0]+pitch[0], cons[1]+vs[1]+pitch[1]+dot_char+vs[2]+'`') \
                    for cons, vs, pitch in \
                    itertools.product(gen_cons, vow_sups, no_pitch)]

#[Vow][Sup]p
vowsup = [(vs[0]+pitch[0], vs[1]+vs[2]+pitch[1]) \
                    for vs, pitch in \
                    itertools.product(vow_sups, no_pitch)]

#-----------------------
# WITH "S"
# with vowel
#(C|many C)Vp.s
cons_vow_s = [(cons[0]+vowel[0]+"s"+pitch[0], cons[1]+vowel[1]+pitch[1]+dot_char+"厶`") \
                    for cons, vowel, pitch in \
                    itertools.product(gen_cons, vowels, no_pitch)]

#Vp.s
vow_s = [(vowel[0]+"s"+pitch[0], \
          vowel[1]+"厶"+pitch[1]) \
            for vowel, pitch in \
            itertools.product(vowels, no_pitch)]

# with vowel suppl
#(C|many C)[Vow]p.[Sup]s
cons_vs_s = [(cons[0]+vs[0]+"s"+pitch[0], cons[1]+vs[1]+pitch[1]+dot_char+vs[2]+"厶") \
                    for cons, vs, pitch in \
                    itertools.product(gen_cons, vow_sups, no_pitch)]
#[Vow]p.[Sup]s
vs_s = [(vs[0]+"s"+pitch[0], \
          vs[1]+'`'+pitch[1]+dot_char+vs[2]+"厶") \
            for vs, pitch in \
            itertools.product(vow_sups, no_pitch)]

# helpers for *VC* combos
v_c_combos = \
list(itertools.chain(itertools.product(pure_vowels, end_cons),
                itertools.product(vow_vows, consonants),
                vEnd_c_iterator)) # for vow w/ cons end
v_cc_combos = \
list(itertools.chain(itertools.product(pure_vowels + vow_vows, multi_end_cons), vEnd_cc_iterator))
vs_c_combos = list(vs_c_iterator)
vs_cc_combos = list(vs_cc_iterator)

# "CVC"
# without s
# with start cons
#(C|many C)Vp.C + (C|many C)Vp.CC
make_cons_vow_cons = lambda vc_comb, tilde: \
[(cons[0]+vc[0][0]+vc[1][0]+pitch[0], cons[1]+vc[0][1]+pitch[1]+dot_char+vc[1][1]+tilde) \
                    for cons, vc, pitch in \
                    itertools.product(gen_cons, vc_comb, no_pitch)]

cons_vow_cons = make_cons_vow_cons(v_c_combos, "`")
cons_vow_mcons = make_cons_vow_cons(v_cc_combos, "")

# (C|many C)[Vow]p.[Sup]C
cons_vs_cons = [(cons[0]+Vs_C[0][0]+Vs_C[1][0]+pitch[0], cons[1]+Vs_C[0][1][0]+pitch[1]+dot_char+Vs_C[0][1][1]+Vs_C[1][1]) \
                    for cons, Vs_C, pitch in \
                    itertools.product(gen_cons, vs_c_combos, no_pitch)]

# (C|many C)[Vow]p.[Sup]C.C
cons_vs_mcons = [(cons[0]+Vs_C[0][0]+Vs_C[1][0]+pitch[0],
               cons[1]+Vs_C[0][1][0]+pitch[1]+dot_char+\
               Vs_C[0][1][1]+Vs_C[1][1][0]+dot_char+\
               Vs_C[1][1][1] + "`") \
                    for cons, Vs_C, pitch in \
                    itertools.product(gen_cons, vs_cc_combos, no_pitch)]

# with no start cons
#VCp
vow_cons = [(v_c[0][0]+v_c[1][0]+pitch[0],
             v_c[0][1]+v_c[1][1]+pitch[1]) \
                    for v_c, pitch in \
                    itertools.product(v_c_combos, no_pitch)]

#VCp.C
vow_mcons = [(v_cc[0][0]+v_cc[1][0]+pitch[0], v_cc[0][1]+v_cc[1][1][0]+pitch[1]+dot_char+v_cc[1][1][1]+'`') \
                    for v_cc, pitch in \
                    itertools.product(v_cc_combos, no_pitch)]

#[Vow][Sup]p.C + [Vow][Sup]p.CC
make_vs_cons = lambda vc_combos, dot: \
 [(vs_c[0][0]+vs_c[1][0]+pitch[0],
    vs_c[0][1]+pitch[1]+dot_char+vs_c[1][1]+dot) \
            for vs_c, pitch in \
            itertools.product(vc_combos, no_pitch)]
vs_cons = make_vs_cons(vs_c_combos, "`") + \
          make_vs_cons(vs_cc_combos, "")


# with s
# with start cons
#(C|many C)Vp.Cs
cons_vow_cons_s = [(cons[0]+v_c[0][0]+v_c[1][0]+"s"+pitch[0], cons[1]+v_c[0][1]+pitch[1]+dot_char+v_c[1][1]+"厶") \
                    for cons, v_c, pitch in \
                    itertools.product(gen_cons,
                                      v_c_combos,
                                      no_pitch)]

#(C|many C)Vp.CC.s
cons_vow_mcons_s = \
 [(cons[0]+v_cc[0][0]+v_cc[1][0]+"s"+pitch[0],
    cons[1]+v_cc[0][1]+pitch[1]+dot_char+\
    v_cc[1][1]+dot_char+"厶`") \
                    for cons, v_cc, pitch in \
                    itertools.product(gen_cons, v_cc_combos, no_pitch)]

#(C|many C)[Vow]p.[Sup]C.s
cons_vs_cons_s = \
[(cons[0]+vs_c[0][0]+vs_c[1][0]+"s"+pitch[0],
  cons[1]+vs_c[0][1][0]+pitch[1]+dot_char+\
  vs_c[0][1][1]+vs_c[1][1]+dot_char+'厶`') \
    for cons, vs_c, pitch in \
    itertools.product(gen_cons,
                      vs_c_combos,
                      no_pitch)
]

#(C|many C)[Vow]p.[Sup]C.Cs
cons_vs_mcons_s = \
[(cons[0]+vs_cc[0][0]+vs_cc[1][0]+"s"+pitch[0],
  cons[1]+vs_cc[0][1][0]+pitch[1]+dot_char+\
  vs_cc[0][1][1]+vs_cc[1][1][0]+dot_char+\
  vs_cc[1][1][1]+'厶') \
    for cons, vs_cc, pitch in \
    itertools.product(gen_cons,
                      vs_cc_combos,
                      no_pitch)
]

# with no start cons
#VCp.s
vow_cons_s = [(v_c[0][0]+v_c[1][0]+"s"+pitch[0],
               v_c[0][1]+v_c[1][1]+pitch[1]+dot_char+"厶`") \
                    for v_c, pitch in \
                        itertools.product(v_c_combos, no_pitch)]

#[Vow][Sup]p.Cs
vs_cons_s = [(vs_c[0][0]+vs_c[1][0]+"s"+pitch[0],
               vs_c[0][1]+pitch[1]+dot_char+\
               vs_c[1][1]+"厶") \
                    for vs_c, pitch in \
                        itertools.product(vs_c_combos, no_pitch)]

#VCp.Cs
vow_mcons_s = [(v_cc[0][0]+v_cc[1][0]+"s"+pitch[0],
                     v_cc[0][1]+v_cc[1][1][0]+pitch[1]+dot_char+\
                     v_cc[1][1][1]+"厶") \
                        for v_cc, pitch in \
                        itertools.product(v_cc_combos, no_pitch)]

#[Vow][Sup]p.CC.s
vs_mcons_s = [(vs_cc[0][0]+vs_cc[1][0]+"s"+pitch[0],
               vs_cc[0][1]+pitch[1]+dot_char+\
               vs_cc[1][1]+dot_char+\
               "厶`") \
                    for vs_cc, pitch in \
                        itertools.product(vs_cc_combos, no_pitch)]


cons_vow_vow = [('saa aa','厶乍乍'),('sei aa','厶丌乍'),
                ('saa1 aa6','厶乍乍'),('sei3 aa6','厶丌乍')]

hng = [('hng'+pitch[0],'亾爻'+pitch[1]) for pitch in pitches_opt]

common_pairs = cons_vow + vow + cons_vs + vowsup + cons_vow_s + vow_s + cons_vs_s + vs_s + cons_vow_cons + cons_vow_mcons + cons_vs_cons + cons_vs_mcons + vow_cons + vow_mcons + vs_cons + cons_vow_cons_s + cons_vow_mcons_s + cons_vs_cons_s + cons_vs_mcons_s + vow_cons_s + vs_cons_s + vow_mcons_s + vs_mcons_s + cons_vow_vow + ng_cons + hng

### Mandarin and Hakka combinations
# ㄦ
ㄦ = [('er'+pitch[0],'ㄦ'+pitch[1]) for pitch in pitches_opt]
# 艮, 亇, 止
艮亇止 = [(ext_vow[0]+pitch[0], ext_vow[1]+pitch[1]) \
          for ext_vow, pitch in itertools.product(ext_vows, pitches_opt)]
# [C w/ r,v]艮 + [C w/ r,v]亇 (v is optional here tbh)
consrv_艮亇 = [(cons[0]+vowel[0]+pitch[0], cons[1]+vowel[1]+pitch[1])
for cons, vowel, pitch in itertools.product(consonants+ext_cons, e_en, pitches_opt)]
# Cw艮
cons_禾艮 = [(cons[0]+"wen"+pitch[0], cons[1]+"禾艮"+pitch[1])
for cons, pitch in itertools.product(consonants, pitches_opt)]
# [r,v]V
rv_vow = [(cons[0]+vowel[0]+pitch[0], cons[1]+vowel[1]+pitch[1]) \
          for cons, vowel, pitch in itertools.product(ext_cons, vowels, pitches_opt)]
# [z, c, s, zh, ch, sh, r] x z
zcsrh_vow = [(cons[0]+'z'+pitch[0],cons[1]+'止'+pitch[1]) for cons, pitch in itertools.product(zcs+zcsh+r_only, pitches_opt)]
### CONSONANT CLUSTERS
# [mw, lw, rw, hj, nj, lj, ngj, zh, ch, zhw, chw] x V
cons_clusters = [(cons[0]+vowel[0]+pitch[0],cons[1]+vowel[1]+pitch[1]) for cons, vowel, pitch in itertools.product(two_cons_aug2 + three_cons_2, vowels, pitches_opt)]
# [j, n, l, z, c, s] x yue
cons_仒旡 = [(cons[0]+'yue'+pitch[0],cons[1]+'仒旡'+pitch[1]) for cons, pitch in itertools.product(cons_yue, pitches_opt)]
# [j, l, z, c, s] x yuen
cons_仒円 = [(cons[0]+'yuen'+pitch[0],cons[1]+'仒円'+pitch[1]) for cons, pitch in itertools.product(cons_yuen, pitches_opt)]
# for keyboard: [z, c, s] x 止 x [m, n, p, t]
zcs_止_mnpt = [(cons[0]+'z'+pitch[0]+cons2[0],
                cons[1]+'止'+pitch[1]+dot_char+cons2[1]+'`') \
            for cons, pitch, cons2 in itertools.product(zcs, pitches_opt, mnpt)]

repeats = [('R'+pitch[0],'々'+pitch[1]) for pitch in pitches_opt]

common_pairs += ㄦ + 艮亇止 + consrv_艮亇 + cons_禾艮 + rv_vow + zcsrh_vow \
            + cons_clusters + cons_仒旡 + cons_仒円 + zcs_止_mnpt + repeats

# add dots
common_pairs = [(ins, outs + dot_char) for ins, outs in common_pairs]

pairs_dict = {}
for pair in common_pairs:
    letters, chars = pair[0], pair[1]
    if letters not in pairs_dict:
        pairs_dict[letters] = list()
    pairs_dict[letters].append(chars)

# keep unique chars while maintaining order in which chars are added
pairs_dict = {letters: list(OrderedDict.fromkeys(outs_list)) for letters, outs_list in pairs_dict.items()}

# printing
# web version
print("""# Rime dictionary
# encoding: utf-8

---
name: jyutcitzi_web
version: "2"
sort: by_weight
use_preset_vocabulary: true
max_phrase_length: 7
min_phrase_weight: 100
import_tables:
  - jyutcitzi_core.lettered
  - jyutcitzi_web.lettered
  - jyutcitzi_web.compound
  - jyutcitzi_web.jyutcit_phrases
  - jyutcitzi_web.phrase
  - jyut6ping3
  - jyut6ping3.phrase
...
""")

for letters, out_set in pairs_dict.items():
    for char in out_set:
        if letters[-1].isalpha():
            print(char, letters, "25000.0", sep="\t")
        else:
            print(char, letters, "20000.0", sep="\t")
