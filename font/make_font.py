#!/usr/local/bin/fontforge
import itertools
from chars import *

# WARNING: use the fontforge interpreter to run the code!!!

# todo list:
# create character for coe
# create character for opposite of 'right'


# \uf8ff is reserved for apple symbol
import fontforge
def add_glyph_to_font(font, hex_val, filename):
    # assert hex_val >= 0xe000 and hex_val < 0xf8ff
    glyph = font.createChar(hex_val, "uni" + hex(hex_val)[2:].upper())
    glyph.clear() # to overwrite existing characters
    glyph.importOutlines(filename)
    glyph.width = 1024
    return glyph
# 'Bold', 'ExtraLight', 'Heavy', 'Light', 'Medium', 'Regular',
for mode in ['PMingLiU']:
    if mode == 'Bland':
        font = fontforge.font()
        font.familyname = "Jyutcitzi"
        font.sfnt_names = ()
        font.weight = "Regular"
        font.fullname = font.familyname# + " Light with JyutCitZi"
        font.fontname = font.familyname
    elif mode == 'PMingLiU':
        font = fontforge.open('./font/mingliu/PMingLiU-02.ttf')
        font.familyname = "JyutcitziWithPMingLiU"
        font.sfnt_names = ()
        font.weight = "Regular"
        font.fullname = font.familyname# + " Light with JyutCitZi"
        font.fontname = font.familyname
    else:
        font = fontforge.open('./font/pingfang/original/PingFang '+mode+'.ttf') # fontforge.font()
    # font.familyname = "PingFang SC"
    # font.sfnt_names = ()
    # font.weight = "LightWithJyutCitZi"
    # font.fullname = font.familyname + " Light with JyutCitZi"
    # font.fontname = "PingFangSCLightWithJyutCitZi"


    font.em = 1024
    hex_val = 0xe000

    # cons only
    for cons in consonants:
        assert hex_val < 0xf8ff
        print(hex(hex_val), cons[1]+"`")
        add_glyph_to_font(font, hex_val,
                          './font/orig_chars/only/cons/' + cons[1] + '`.svg')
        hex_val += 1

    #ng
    print(hex(hex_val), 'ng`')
    add_glyph_to_font(font, hex_val,
                      './font/orig_chars/only/cons/ng`.svg')
    hex_val += 1
    #m
    print(hex(hex_val), 'm`')
    add_glyph_to_font(font, hex_val,
                      './font/orig_chars/only/cons/m`.svg')
    hex_val += 1

    #ng_m
    ng_m_val = 0x20121 # compabtibility with glyphwiki
    print(hex(ng_m_val), 'ng_m')
    add_glyph_to_font(font, ng_m_val,
                      './font/orig_chars/cons/ng.svg')

    # vowel only
    for vowel in vowels:
        assert hex_val < 0xf8ff
        print(hex(hex_val), vowel[1]+"`")
        vow = "oe" if vowel[1] == '居' else vowel[1]
        add_glyph_to_font(font, hex_val,
                          './font/orig_chars/only/vows/' + vow + '`.svg')
        hex_val += 1

    # cons + vowel
    for cons, vowel in itertools.product(consonants, vowels):
        assert hex_val < 0xf8ff
        print(hex(hex_val), cons[1] + vowel[1])
        vow = "oe" if vowel[1] == '居' else vowel[1]
        add_glyph_to_font(font, hex_val,
                          "./font/orig_chars/cons_vows/" + cons[1] + vow +".svg")
        hex_val += 1

    # cons + cons + vowel
    for cons, vowel in itertools.product(two_cons, vowels):
        assert hex_val < 0xf8ff
        print(hex(hex_val), cons[1] + vowel[1])
        vow = "oe" if vowel[1] == '居' else vowel[1]
        add_glyph_to_font(font, hex_val,
                          "./font/orig_chars/two_cons_vows/" + cons[1] + vow +".svg")
        hex_val += 1

    # cons + vowel + vowel
    assert hex_val < 0xf8ff
    print(hex(hex_val), '厶乍乍')
    add_glyph_to_font(font, hex_val,
                      "./font/orig_chars/cons_two_vows/厶乍乍.svg")
    hex_val += 1

    # special characters
    for _, spec_char in spec_uni_particles + spec_uni_phrases + spec_uni_phrases_2:
        assert hex_val < 0xf8ff
        print(hex(hex_val), spec_char)
        add_glyph_to_font(font, hex_val,
                          "./font/orig_chars/special_chars/combined/" +spec_char+".svg")
        hex_val += 1

    # 正_flip
    assert hex_val < 0xf8ff
    print(hex(hex_val), '正_flip')
    add_glyph_to_font(font, hex_val,
                      "./font/orig_chars/special_chars/parts/正_flip.svg")
    hex_val += 1

    ## ======= second Version =========
    vow_t = lambda v_char: 'oe' if v_char == '居' else v_char
    cons_t = lambda c_char: '爻_tb' if c_char == '爻' else c_char

    # more CCV
    for two_con, vowel in itertools.product(two_cons_aug, vowels):
        assert hex_val < 0xf8ff
        print(hex(hex_val), two_con[1] + vow_t(vowel[1]))
        add_glyph_to_font(font, hex_val,
                          "./font/orig_chars/two_cons_vows/" + two_con[1] + vow_t(vowel[1]) +".svg")
        hex_val += 1

    # (three_cons)V (10*56) => 616
    for conses, vowel in itertools.product(three_cons, vowels):
        assert hex_val < 0xf8ff
        chars = conses[1] + vow_t(vowel[1])
        print(hex(hex_val), chars)
        add_glyph_to_font(font, hex_val,
                          "./font/orig_chars/three_cons_vow/"+chars+".svg")
        hex_val += 1

    # VC + VS + VowSup => all VC 1176
    for cons, vowel in itertools.product(consonants, vowels):
        assert hex_val < 0xf8ff
        print(hex(hex_val), vow_t(vowel[1]) + cons[1])
        add_glyph_to_font(font, hex_val,
                          "./font/orig_chars/vows_cons/" + vow_t(vowel[1]) + cons[1] +".svg")
        hex_val += 1

    # CC + CS + SupS + SupC => all CC (21*21) = 441
    for cons, cons2 in itertools.product(consonants, consonants):
        assert hex_val < 0xf8ff
        print(hex(hex_val), cons[1] + cons2[1])
        add_glyph_to_font(font, hex_val,
                          "./font/orig_chars/cons_cons/" + cons[1] + cons2[1] +".svg")
        hex_val += 1

    # cons + vowel + vowel
    assert hex_val < 0xf8ff
    print(hex(hex_val), '厶丌乍')
    add_glyph_to_font(font, hex_val,
                      "./font/orig_chars/cons_two_vows/厶丌乍.svg")
    hex_val += 1

    # print("uni"+hex(0xe000)[2:].upper())
    # glyph = font.createChar(0xe000, "uni" + hex(0xe000)[2:].upper())
    # glyph.importOutlines("./fire.svg")
    # glyph.width = 1024
    #
    # glyph = font.createChar(0xe001, "uni" + hex(0xe001)[2:].upper())
    # glyph.importOutlines("./skip.svg")
    # glyph.width = 1024

    # print(glyph.glyphname, glyph.width)
    if mode == 'Bold':
        print(font)
    font.autoWidth(150)
    if mode == 'Bland':
        font.generate("./font/pingfang/augmented/Jyutcitzi.ttf")
    elif mode == 'PMingLiU':
        font.generate("./font/pingfang/augmented/Jyutcitzi (PMingLiU).ttf")
    else:
        font.generate("./font/pingfang/augmented/PingFang "+mode+".ttf")
    font.close()
