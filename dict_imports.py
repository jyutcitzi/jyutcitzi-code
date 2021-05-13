import copy
from font.chars import *
import itertools
from collections import OrderedDict

# construct chars to hex dictionary
## version 1: "./font/orig_chars/hex_to_chars.txt"
hex_dict = get_hex_dict("./font/fonts/mapping.txt", ng_tilde=False)

pitches_opt = pitches_only+[('','')]
cons_vow_dict = {cons[0]+vowel[0]+pitch[0]: cons[1]+vowel[1]+pitch[1] \
                    for cons, vowel, pitch in \
                    itertools.product(consonants+many_cons, vowels, pitches_opt)}
ng_dict = {pair[0] + pitch[0]: pair[1] + pitch[1] for pair, pitch in itertools.product(special_cons, pitches_opt)}

vow_dict = {vowel[0]+pitch[0]: vowel[1]+"`"+pitch[1] for vowel, pitch in itertools.product(vowels, pitches_opt)}

specials = {"kom1": "臼个¯·文`", "kom": "臼个·文`",
            "kop1": "臼个¯·并`", "kop": "臼个·并`",
            "fom1": "夫个¯·文`", "fom": "夫个·文`",
            "gwup1": "古乎¯·并`", "gwup": "古乎·并`",
            "top1": "天个¯·并`", "top": "天个·并`",
            "tup1": "天乎¯·并`", "tup": "天乎·并`",
            "sum1": "厶乎¯·文`", "sum": "厶乎·文`",
            "zop1": "止个¯·并`", "zop": "止个·并`",
            "cop1": "此个¯·并`", "cop": "此个·并`",
            "ng3aa5": "爻``·乍`˝", "ng3aa": "爻`·乍`",
            "ng3aa4": "爻``·乍`⁼", "ng3aa": "爻`·乍`"}
repeat = {"[repeat]": "々"}

mapping = {**cons_vow_dict, **ng_dict, **vow_dict,
            **specials, **repeat}

def syl_pitch_to_char_pitch(syl_pitch):
    if syl_pitch in hex_dict:
        return hex_dict[syl_pitch]
    else:
        return syl_pitch

    # has_pitch = syl_pitch[-1] in [p[1] for p in pitches_only]
    # if has_pitch:
    #     return hex_dict[syl_pitch[:-1]]+syl_pitch[-1]
    # else: # no pitch
    #     if syl_pitch in hex_dict:
    #         return hex_dict[syl_pitch]
    #     else:
    #         return syl_pitch
    #     # elif len(syl_pitch) == 1: # probably a honzi
    #     #     return syl_pitch
    #     # else:
    #     #     return "[ERROR]"

def has_goigaakhonzi(tgt):
    for honzi in [x[0] for x in goigaakhonzi] + ['咩','咪']:
        if honzi in tgt:
            return True
    return False

def get_tgts(file_loc):
    ret_list = []
    with open(file_loc) as file:
        for line in file.readlines():
            ret_list.append(line[:-1].split('\t')[0])
    return ret_list

羋_list = get_tgts("./rime/改革漢字/羋.txt")
袂_list = get_tgts("./rime/改革漢字/袂.txt")
旡_list = get_tgts("./rime/改革漢字/羋.txt")
丩旡_list = get_tgts("./rime/改革漢字/袂.txt")

vowels_extended = vowels + [('a','乍')]
cv_dict = {cons[0]+vow[0]: cons[1]+vow[1] \
                    for cons, vow in itertools.product(consonants, vowels_extended)}
v_dict = {vow[0]: vow[1]+'`' for vow in vowels}
latin_to_glyph = {**cv_dict, **v_dict}
eng_num_jyutping_syll = {'book': 1, "camp-camp-": 2, "p": 1,
                         "all-back": 2, "A-math": 2, "an": 1,
                         "A4": 2, "AA": 2, "AB": 2, "AV": 2, "A": 1,
                         "Band": 1, "Bang": 1, "BB": 2, 'bell': 1, "Ben": 1,
                         "bibu": 2, "boot": 1, "boxing": 2, "bu": 1, "B": 1,
                         "café": 2, "call": 1, "Call": 1, "cam": 1, 'cap': 1,
                         'chalk': 1, 'cheap': 1, 'check': 1, 'chok': 1, 'chord': 1,
                         'chup': 1, 'claim': 1, 'click': 1, 'cue': 1, 'cut': 1, 'C': 1, "DNA": 3, 'down': 1, 'Do': 1, 'due': 1, 'dum': 1, 'dup': 1, 'dur': 1, 'D': 1, 'er': 1, 'EVA': 3, 'E': 1, 'fan': 1, 'fax': 2, 'Fing': 1, 'fit': 1, 'foul': 1, 'free': 1, 'friend': 1, 'band': 1, 'gap-gap': 2, 'gas': 1, 'gel': 1, 'get': 1, 'geot-geot': 2, 'goet-goet': 2, 'Google': 2, 'guard': 1, 'gym': 1, 'G': 1, 'hang': 1, 'Hap': 1, 'Happy': 2, 'high': 1, 'hum-hum': 2, 'H': 1, 'IQ': 2, 'IT': 2, 'i': 1, 'jam': 1, 'jeep': 1, 'jer': 1, 'jupas': 2, 'J': 1, 'kai': 1, 'keep': 1, 'kem-kem': 2, 'K': 1, 'lag': 1, 'lai-lai': 2, 'LAN': 1, 'lin': 1, 'mag': 1, 'Mark': 1, 'mark': 1, 'MK': 1, 'mon': 1, 'M': 1, 'ngang-ngang': 2, 'ngok-ngok': 2, 'N': 1, 'OK': 2, 'on9': 2, 'over': 2, 'O': 1, 'PE': 2, 'pH': 2, 'pu': 1, 'P': 1, 'Q': 1, 'Roll': 1, 'set': 1, 'sharp': 1, 'short-short': 2, 'Short': 1, 'sink': 1, 'sorry': 2, 'style': 2, 'sub': 1, 'take': 1, 'talk': 1, 'tup': 1, 'T': 1, 'USB': 3, 'U': 1, 'van': 1, 'V': 1, 'wet': 1, 'XO': 2, 'X': 1, 'YP': 2, 'ger': 1, 'head': 1, 'sir': 1, 'cool': 1, 'seed': 1, 'fun': 1, 'leu': 1, 'roller': 2, 'cheat': 1, 'pool': 1, 'show': 1, 'liu': 1, 'fd': 1, 'watt': 1, 'L': 1, 'like': 1, 'ti': 1, 'party': 2, 'jel-jel': 2, 'pop': 1, 'power': 1, 'quali': 2, 'grade': 1, 'pay': 1, 'Yeah': 1, 'key': 1, 'plan': 1, 'nan1': 1, 'pan': 1, 'board': 1, 'gag': 1, 'job': 1, 'cheque': 1, 'OT': 2, 'turbo': 2, 'belt': 1, 'ling': 1, 'full': 1, 'mood': 1, 'point': 1, 'say': 1, 'LOOK': 1, 'open-day': 3, 'keng': 1, 'a': 1, 'pok': 1, 'post': 1, 'gwe': 1, 'cancer': 2, 'port': 1, 'do': 1, 'die': 1, 'pat-pat': 2, 'QQ': 2, 'sem': 1, 'LINE': 1, 'SM': 2, 'beyond': 2, 'day': 1, 'feel': 1, 'chop': 1,
                         'heart': 1, 'so': 1, 'lift': 1, 'gay': 1, 'plan': 1, 'Plan': 1, 'dog-dog': 2, 'qq': 2, 'po': 1, 'box': 1, 'lab': 1, 'part-time': 2, 'show': 1,
                         }
pitch_dict = {num: pitch for num, pitch in pitches_only}

def do_the_replace(tgt_old, replace_arr, char):
    replace_idx = 0
    tgt_new = ""
    for t_char in tgt_old:
        if t_char == char:
            tgt_new += replace_arr[replace_idx]
            replace_idx += 1
        else:
            tgt_new += t_char
    return tgt_new

op_ends = {'zop': ('止个','并`'),
           'cop': ('此个','并`')}
def jyutping_to_proper_char(jyutping, with_pitch):
    pitch_str = pitch_dict[jyutping[-1]] if with_pitch else ""
    if jyutping[:-1] in op_ends:
        first, second = op_ends[jyutping[:-1]]
        font_char = hex_dict[first+pitch_str]+hex_dict[second]
        web_char = dot_char+first+pitch_str+dot_char+second+dot_char
    else:
        glyph = latin_to_glyph[jyutping[:-1]]
        font_char = hex_dict[glyph+pitch_str]
        web_char = dot_char+glyph+pitch_str+dot_char
    return font_char, web_char


def context_aware_replace(tgt_web, tgt_font, src_arr, char, with_pitch=True):
    blacklist_chars = ["…","，"]+[p[1] for p in pitches_only]
    if any(x in tgt_font for x in blacklist_chars):
        tgt_temp = list(tgt_font)
        for c in blacklist_chars:
            if c in tgt_temp:
                tgt_temp.remove(c)
    else:
        tgt_temp = tgt_font
    assert len(src_arr) == len(tgt_temp)
    assert tgt_font.count(char) == tgt_web.count(char)

    # get the jyutping for the character to be replaced
    # in each instance of the character
    replace_web = []
    replace_font = []
    for jyutping, t_char in zip(src_arr, list(tgt_temp)):
        if t_char == char:
            assert jyutping[-1] in pitch_dict
            font_char, web_char = jyutping_to_proper_char(jyutping, with_pitch)
            replace_font.append(font_char)
            replace_web.append(web_char)

    new_tgt_web = do_the_replace(tgt_web, replace_web, char)
    new_tgt_font = do_the_replace(tgt_font, replace_font, char)
    return new_tgt_font, new_tgt_web

more_chars = ['-','é']
def eng_to_jcz(tgt, src_arr, with_pitch=False):
    # parse
    if any(c.encode('utf-8').isalpha() for c in tgt):
        new_tgt_web, new_tgt_font, eng_word = "", "", ""
        src_idx, tgt_idx = 0, 0
        while tgt_idx < len(tgt):
            word = ""
            if tgt[tgt_idx].encode('utf-8').isalpha() or tgt[tgt_idx] == '-':
                while tgt[tgt_idx].encode('utf-8').isalnum() or tgt[tgt_idx] in more_chars:
                    word += tgt[tgt_idx]
                    tgt_idx += 1
                    if tgt_idx == len(tgt):
                        break
                if word != "": # construct jcz
                    num_syl = eng_num_jyutping_syll[word]
                    while num_syl > 0:
                        syl = src_arr[src_idx]
                        assert syl[-1].isdigit()
                        font_char, web_char = jyutping_to_proper_char(syl, with_pitch)
                        # glyph = latin_to_glyph[syl[:-1]]
                        # pitch_str = pitch_dict[syl[-1]] if with_pitch else ""
                        new_tgt_web += web_char
                        new_tgt_font += font_char
                        # decrement
                        src_idx += 1
                        num_syl -= 1
            else:
                new_tgt_web += tgt[tgt_idx]
                new_tgt_font += tgt[tgt_idx]
                src_idx += 1
                tgt_idx += 1
        return new_tgt_font, new_tgt_web
    else:
        return tgt, tgt

def tgt2webandfont(tgt, src):
    src_arr = src.split() # split by whitespace

    # 1. get rid of all "English" in phrases
    # keep uppercase characters and digits
    # replace all lowercase letters with jcz

    if len(src_arr) > 0:
        tgt_font, tgt_web = eng_to_jcz(tgt, src_arr, with_pitch=False)
    else:
        tgt_font, tgt_web = tgt, tgt

    if tgt in 羋_list:
        tgt_font = tgt_font.replace("咩", "羋")
        tgt_web = tgt_web.replace("咩", "羋")
    else:
        tgt_font = tgt_font.replace("咩", hex_dict["文旡¯"])
        tgt_web = tgt_web.replace("咩", dot_char + "文旡¯" + dot_char)
    if tgt in 袂_list:
        tgt_font = tgt_font.replace("咪", "袂")
        tgt_web = tgt_web.replace("咪", "袂")
    if tgt in 旡_list:
        tgt_font = tgt_font.replace("嘅", "旡")
        tgt_web = tgt_web.replace("嘅", "旡")
    if tgt == "報紙登嘅消息全部係堅嘅":
        # special case with two different ge's
        tgt_font = "報紙登旡消息全部係堅"+hex_dict["丩旡"]
        tgt_web = "報紙登旡消息全部係堅"+dot_char+"丩旡"+dot_char
    if tgt in 丩旡_list:
        tgt_font = tgt_font.replace("嘅", hex_dict["丩旡"])
        tgt_web = tgt_web.replace("嘅", dot_char+"丩旡`"+dot_char)

    if len(src_arr) > 0:
        for char in contested_chars:
            if char in tgt:
                # we need to figure out which jcz to use via src
                tgt_font, tgt_web = context_aware_replace(tgt_web, tgt_font, src_arr, char, with_pitch=True)
    else: # no source to refer to => make an educated guess
        for orig_c, web_c, font_c in gghz_guess:
            if len(web_c) > 1:
                tgt_web = tgt_web.replace(orig_c, dot_char + web_c + dot_char)
            else: # some may be honzi
                tgt_web = tgt_web.replace(orig_c, web_c)
            tgt_font = tgt_font.replace(orig_c, font_c)


    for orig_c, web_c, font_c in goigaakhonzi:
        if len(web_c) > 1:
            tgt_web = tgt_web.replace(orig_c, dot_char + web_c + dot_char)
        else: # some may be honzi
            tgt_web = tgt_web.replace(orig_c, web_c)
        tgt_font = tgt_font.replace(orig_c, font_c)

    # postprcoess dots in tgt_web
    tgt_web = tgt_web.replace("··" ,"·")
    if tgt_web[0] == "·":
        tgt_web = tgt_web[1:]
    return tgt_font, tgt_web

# tgt_font, tgt_web = context_aware_replace("夠時候·力乍¯·咯","夠時候啦咯","gau3 si4 hau6 laa1 lok3".split(),"咯",with_pitch=True)
# print(tgt_font, tgt_web)


# Q: should we offer repetition as an option?
# gep々聲 in addition to gepgep聲 (lettered; font and web)
# 黃黚々 in addition to 黃黚黚 (compound; core, font and web)
# [phrase] (phrase; font and web)
def has_repetition(tgt):
    for i in range(len(tgt)-1):
        if tgt[i] == tgt[i+1]:
            return True
    return False

# def remove_repetition(tgt):
#     new_tgt = ""
#     word = tgt[0]
#
#     for i in range(len(tgt)):
