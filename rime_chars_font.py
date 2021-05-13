# TODO:
# leaving double vowels out for now
# add # character (do this by changing encode in lang file)

# command for generating font file (in UTF-16)
# e.g. python rime_chars_font.py > jyutcitzi_font.dict.yaml

from font.chars import *
from font.chars_vowel import vEnd_c_iterator, \
                             vEnd_cc_iterator, \
                             vs_c_iterator, \
                             vs_cc_iterator
import itertools
from collections import OrderedDict

# construct chars to hex dictionary
# note that ng_tilde = TRUE
hex_dict = get_hex_dict("./font/fonts/mapping.txt", ng_tilde=True)

ng_m_chars = [("ng",chr(0x20121)), ("m",chr(0x20121))]

ngs_chars = [("ng","ng`"), ("m","m`")]

# make pitches optional
pitches_opt = [('','')] + pitches_only #
no_pitch = [('','')]

ng_cons_chars = [(ng[0]+pitch[0], ng[1]+pitch[1]) \
            for ng, pitch in itertools.product(ng_m_chars, pitches_opt)]
ng_cons_chars += [(ng[0]+pitch[0], hex_dict[ng[1]+pitch[1]]) \
            for ng, pitch in itertools.product(ngs_chars, pitches_opt)]

gen_cons_opt_pitch = consonants + r_only + many_cons_opt_pitch
gen_cons_no_pitch = many_cons_no_pitch
gen_cons = gen_cons_opt_pitch + gen_cons_no_pitch
def get_gen_cons_vowel_itr(some_vowels):
    return itertools.chain.from_iterable(
                [itertools.product(gen_cons_opt_pitch, some_vowels, pitches_opt),
                itertools.product(gen_cons_no_pitch, some_vowels, no_pitch)])

# ---------------
# NO "S"
#(C|many C)Vp

cons_vow_chars = [(cons[0]+vowel[0]+pitch[0],
             hex_dict[cons[1]+vowel[1]+pitch[1]]) \
                    for cons, vowel, pitch in \
                    get_gen_cons_vowel_itr(vowels)]
                    # itertools.product(gen_cons, vowels, pitches_opt)

#Vp
vow_chars = [(vowel[0]+pitch[0], hex_dict[vowel[1]+'`'+pitch[1]]) \
                    for vowel, pitch in \
                    itertools.product(vowels, pitches_opt)]

#(C|many C)[Vow]p.[Sup]
cons_vs_chars = [(cons[0]+vs[0]+pitch[0], hex_dict[cons[1]+vs[1]+pitch[1]]+hex_dict[vs[2]+'`']) \
                    for cons, vs, pitch in \
                    itertools.product(gen_cons, vow_sups, no_pitch)]
#[Vow][Sup]p
vowsup_chars = [(vs[0]+pitch[0], hex_dict[vs[1]+vs[2]+pitch[1]]) \
                    for vs, pitch in \
                    itertools.product(vow_sups, no_pitch)]

#-----------------------
# WITH "S"
# with vowel
#(C|many C)Vp.s
cons_vow_s_chars = [(cons[0]+vowel[0]+"s"+pitch[0], hex_dict[cons[1]+vowel[1]+pitch[1]]+hex_dict["厶`"]) \
                    for cons, vowel, pitch in \
                    itertools.product(gen_cons, vowels, no_pitch)]

#Vp.s
vow_s_chars = [(vowel[0]+"s"+pitch[0], \
          hex_dict[vowel[1]+"厶"+pitch[1]]) \
            for vowel, pitch in \
            itertools.product(vowels, no_pitch)]

# with vowel suppl
#(C|many C)[Vow]p.[Sup]s
cons_vs_s_chars = [(cons[0]+vs[0]+"s"+pitch[0],
                hex_dict[cons[1]+vs[1]+pitch[1]]+\
                hex_dict[vs[2]+"厶"]) \
                    for cons, vs, pitch in \
                    itertools.product(gen_cons, vow_sups, no_pitch)]
#[Vow]p.[Sup]s
vs_s_chars = [(vs[0]+"s"+pitch[0], \
              hex_dict[vs[1]+'`'+pitch[1]]+\
              hex_dict[vs[2]+"厶"]) \
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
make_cons_vow_cons_chars = lambda vc_comb, tilde: \
[(cons[0]+vc[0][0]+vc[1][0]+pitch[0],
 hex_dict[cons[1]+vc[0][1]+pitch[1]]+\
 hex_dict[vc[1][1]+tilde]) \
                    for cons, vc, pitch in \
                    itertools.product(gen_cons, vc_comb, no_pitch)]
cons_vow_cons_chars = make_cons_vow_cons_chars(v_c_combos,"`")
cons_vow_mcons_chars = make_cons_vow_cons_chars(v_cc_combos,"")

# (C|many C)[Vow]p.[Sup]C
cons_vs_cons_chars = [(cons[0]+Vs_C[0][0]+Vs_C[1][0]+pitch[0],
hex_dict[cons[1]+Vs_C[0][1][0]+pitch[1]]+ \
hex_dict[Vs_C[0][1][1]+Vs_C[1][1]]) \
                    for cons, Vs_C, pitch in \
                    itertools.product(gen_cons, vs_c_combos, no_pitch)]

# (C|many C)[Vow]p.[Sup]C.C
cons_vs_mcons_chars = [(cons[0]+Vs_C[0][0]+Vs_C[1][0]+pitch[0],
       hex_dict[cons[1]+Vs_C[0][1][0]+pitch[1]]+\
       hex_dict[Vs_C[0][1][1]+Vs_C[1][1][0]]+\
       hex_dict[Vs_C[1][1][1] + "`"]) \
            for cons, Vs_C, pitch in \
            itertools.product(gen_cons, vs_cc_combos, no_pitch)]

# with no start cons
#VCp
vow_cons_chars = [(v_c[0][0]+v_c[1][0]+pitch[0],
             hex_dict[v_c[0][1]+v_c[1][1]+pitch[1]]) \
                    for v_c, pitch in \
                    itertools.product(v_c_combos, no_pitch)]

#VCp.C
vow_mcons_chars = [(v_cc[0][0]+v_cc[1][0]+pitch[0],
hex_dict[v_cc[0][1]+v_cc[1][1][0]+pitch[1]]+\
hex_dict[v_cc[1][1][1]+'`']) \
                    for v_cc, pitch in \
                    itertools.product(v_cc_combos, no_pitch)]

#[Vow][Sup]p.C + [Vow][Sup]p.CC
make_vs_cons_chars = lambda vc_combos, tilde: \
 [(vs_c[0][0]+vs_c[1][0]+pitch[0],
    hex_dict[vs_c[0][1]+pitch[1]]+\
    hex_dict[vs_c[1][1]+tilde]) \
            for vs_c, pitch in \
            itertools.product(vc_combos, no_pitch)]
vs_cons_chars = make_vs_cons_chars(vs_c_combos, "`") + \
          make_vs_cons_chars(vs_cc_combos, "")


# with s
# with start cons
#(C|many C)Vp.Cs
cons_vow_cons_s_chars = [(cons[0]+v_c[0][0]+v_c[1][0]+"s"+pitch[0], hex_dict[cons[1]+v_c[0][1]+pitch[1]]+\
hex_dict[v_c[1][1]+"厶"]) \
                    for cons, v_c, pitch in \
                    itertools.product(gen_cons,
                                      v_c_combos,
                                      no_pitch)]
#(C|many C)Vp.CC.s
cons_vow_mcons_s_chars = [(cons[0]+v_cc[0][0]+v_cc[1][0]+"s"+pitch[0],
   hex_dict[cons[1]+v_cc[0][1]+pitch[1]]+\
   hex_dict[v_cc[1][1]]+hex_dict["厶`"]) \
                   for cons, v_cc, pitch in \
                   itertools.product(gen_cons, v_cc_combos, no_pitch)]


#(C|many C)[Vow]p.[Sup]C.s
cons_vs_cons_s_chars = \
[(cons[0]+vs_c[0][0]+vs_c[1][0]+"s"+pitch[0],
  hex_dict[cons[1]+vs_c[0][1][0]+pitch[1]]+\
  hex_dict[vs_c[0][1][1]+vs_c[1][1]]+'厶`') \
    for cons, vs_c, pitch in \
    itertools.product(gen_cons,
                      vs_c_combos,
                      no_pitch)
]


#(C|many C)[Vow]p.[Sup]C.Cs
cons_vs_mcons_s_chars = \
[(cons[0]+vs_cc[0][0]+vs_cc[1][0]+"s"+pitch[0],
  hex_dict[cons[1]+vs_cc[0][1][0]+pitch[1]]+\
  hex_dict[vs_cc[0][1][1]+vs_cc[1][1][0]]+\
  hex_dict[vs_cc[1][1][1]+'厶']) \
    for cons, vs_cc, pitch in \
    itertools.product(gen_cons,
                      vs_cc_combos,
                      no_pitch)
]

# with no start cons
#VCp.s
vow_cons_s_chars = [(v_c[0][0]+v_c[1][0]+"s"+pitch[0],
               hex_dict[v_c[0][1]+v_c[1][1]+pitch[1]]+hex_dict["厶`"]) \
                    for v_c, pitch in \
                        itertools.product(v_c_combos, no_pitch)]

#[Vow][Sup]p.Cs
vs_cons_s_chars = [(vs_c[0][0]+vs_c[1][0]+"s"+pitch[0],
               hex_dict[vs_c[0][1]+pitch[1]]+\
               hex_dict[vs_c[1][1]+"厶"]) \
                    for vs_c, pitch in \
                        itertools.product(vs_c_combos, no_pitch)]


#VCp.Cs
vow_mcons_s_chars = [(v_cc[0][0]+v_cc[1][0]+"s"+pitch[0],
                 hex_dict[v_cc[0][1]+v_cc[1][1][0]+pitch[1]]+\
                 hex_dict[v_cc[1][1][1]+"厶"]) \
                    for v_cc, pitch in \
                    itertools.product(v_cc_combos, no_pitch)]

#[Vow][Sup]p.CC.s
vs_mcons_s_chars = [(vs_cc[0][0]+vs_cc[1][0]+"s"+pitch[0],
               hex_dict[vs_cc[0][1]+pitch[1]]+\
               hex_dict[vs_cc[1][1]]+\
               hex_dict["厶`"]) \
                    for vs_cc, pitch in \
                        itertools.product(vs_cc_combos, no_pitch)]


cons_vow_vow_chars = [('saa aa',hex_dict['厶乍乍']),
                      ('sei aa',hex_dict['厶丌乍']),
                      ('saa1 aa6',hex_dict['厶乍乍']),
                      ('sei3 aa6',hex_dict['厶丌乍'])]

hng_chars = [('hng'+pitch[0],hex_dict['亾爻'+pitch[1]]) for pitch in pitches_opt]

# these can't have dots
common_pairs_chars = cons_vow_chars + vow_chars + cons_vs_chars + vowsup_chars + cons_vow_s_chars + vow_s_chars + cons_vs_s_chars + vs_s_chars + cons_vow_cons_chars + cons_vow_mcons_chars + cons_vs_cons_chars + cons_vs_mcons_chars + vow_cons_chars + vow_mcons_chars + vs_cons_chars + cons_vow_cons_s_chars + cons_vow_mcons_s_chars + cons_vs_cons_s_chars + cons_vs_mcons_s_chars + vow_cons_s_chars + vs_cons_s_chars + vow_mcons_s_chars + vs_mcons_s_chars + cons_vow_vow_chars + ng_cons_chars + hng_chars

### Mandarin and Hakka combinations
# ㄦ
ㄦ_chars = [('er'+pitch[0],'ㄦ'+pitch[1]) for pitch in pitches_opt]
# 艮, 亇, 止
艮亇止_chars = [(ext_vow[0]+pitch[0], hex_dict[ext_vow[1]+"`"+pitch[1]]) \
          for ext_vow, pitch in itertools.product(ext_vows, pitches_opt)]
# [C w/ r,v]艮 + [C w/ r,v]亇 (v is optional here tbh)
consrv_艮亇_chars = [(cons[0]+vowel[0]+pitch[0], hex_dict[cons[1]+vowel[1]+pitch[1]])
for cons, vowel, pitch in itertools.product(consonants+ext_cons, e_en, pitches_opt)]
# Cw艮
cons_禾艮_chars = [(cons[0]+"wen"+pitch[0], hex_dict[cons[1]+"禾艮"+pitch[1]])
for cons, pitch in itertools.product(consonants, pitches_opt)]
# [r,v]V
rv_vow_chars = [(cons[0]+vowel[0]+pitch[0], hex_dict[cons[1]+vowel[1]+pitch[1]]) \
          for cons, vowel, pitch in itertools.product(ext_cons, vowels, pitches_opt)]
# [z, c, s, zh, ch, sh, r] x z
zcsrh_vow_chars = [(cons[0]+'z'+pitch[0],hex_dict[cons[1]+'止'+pitch[1]]) for cons, pitch in itertools.product(zcs+zcsh+r_only, pitches_opt)]
### CONSONANT CLUSTERS
# [mw, lw, rw, hj, nj, lj, ngj, zh, ch, zhw, chw] x V
cons_clusters_chars = [(cons[0]+vowel[0]+pitch[0],hex_dict[cons[1]+vowel[1]+pitch[1]]) for cons, vowel, pitch in itertools.product(two_cons_aug2 + three_cons_2, vowels, pitches_opt)]
# [j, n, l, z, c, s] x yue
cons_仒旡_chars = [(cons[0]+'yue'+pitch[0],hex_dict[cons[1]+'仒旡'+pitch[1]]) for cons, pitch in itertools.product(cons_yue, pitches_opt)]
# [j, l, z, c, s] x yuen
cons_仒円_chars = [(cons[0]+'yuen'+pitch[0],hex_dict[cons[1]+'仒円'+pitch[1]]) for cons, pitch in itertools.product(cons_yuen, pitches_opt)]
# for keyboard: [z, c, s] x 止 x [m, n, p, t]
zcs_止_mnpt_chars = [(cons[0]+'z'+pitch[0]+cons2[0],
                hex_dict[cons[1]+'止'+pitch[1]]+hex_dict[cons2[1]+'`']) \
            for cons, pitch, cons2 in itertools.product(zcs, pitches_opt, mnpt)]

repeats_chars = [('R'+pitch[0],hex_dict['々'+pitch[1]]) for pitch in pitches_opt]

common_pairs_chars += ㄦ_chars + 艮亇止_chars + consrv_艮亇_chars \
                    + cons_禾艮_chars + rv_vow_chars + zcsrh_vow_chars \
                    + cons_clusters_chars + cons_仒旡_chars + cons_仒円_chars \
                    + zcs_止_mnpt_chars + repeats_chars

pairs_chars_dict = {}
for pair in common_pairs_chars:
    letters, chars = pair[0], pair[1]
    if letters not in pairs_chars_dict:
        pairs_chars_dict[letters] = list()
    pairs_chars_dict[letters].append(chars)

# keep unique chars while maintaining order in which chars are added
pairs_chars_dict = {letters: list(OrderedDict.fromkeys(outs_list)) for letters, outs_list in pairs_chars_dict.items()}

# printing
# font version
print("""# Rime dictionary
# encoding: utf-8

---
name: jyutcitzi_font
version: "2"
sort: by_weight
use_preset_vocabulary: true
max_phrase_length: 7
min_phrase_weight: 100
import_tables:
  - jyutcitzi_core.lettered
  - jyutcitzi_font.lettered
  - jyutcitzi_font.compound
  - jyutcitzi_font.jyutcit_phrases
  - jyutcitzi_font.phrase
  - jyut6ping3
  - jyut6ping3.phrase
...
""")

for letters, out_set in pairs_chars_dict.items():
    for char in out_set:
        if letters[-1].isalpha():
            print(char, letters, "25000.0", sep="\t")
        else:
            print(char, letters, "20000.0", sep="\t")
