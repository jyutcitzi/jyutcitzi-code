#!/usr/local/bin/fontforge
import itertools
from chars import *
import fontforge
import os
from fonts_config import fonts

# WARNING: use the fontforge interpreter to run the code!!!
# \uf8ff is reserved for apple symbol

# based on letter accents
tonemarks = ['¯','´','`','⁼','˝','ﾞ','\'',"\""]
# based on bpmf tones
# tonemarks = ['¯','ˊ','ˋ','⁼','˝','ﾞ','\'',"\""]

def add_glyph_to_font(font, hex_val, filename):
    # assert hex_val >= 0xe000 and hex_val < 0xf8ff
    glyph = font.createChar(hex_val, "uni" + hex(hex_val)[2:].upper())
    glyph.clear() # to overwrite existing characters
    glyph.importOutlines(filename)
    glyph.width = 1024
    return glyph

record_mapping = True
record_loc = "./fonts/mapping.txt"
for fontname in fonts:
    dirname = fonts[fontname]['folder']
    for weight in fonts[fontname]['weights']:
        print('start ', fontname, weight)
        char_folder = dirname + weight + '/chars/'
        block_folder = dirname + weight + '/blocks/'
        reffontname = fonts[fontname]['referenceFont']
        if reffontname is None:
            # create empty font
            font = fontforge.font()
        else:
            # load reference font
            print(dirname + weight + '/' + reffontname + '-' + weight + '.ttf')
            font = fontforge.open(dirname + weight + '/' + reffontname + '-' + weight + '.ttf')
        font.familyname = "JyutcitziWith" + fontname# + weight
        font.sfnt_names = ()
        font.weight = weight
        font.fullname = font.familyname + weight# + " Light with JyutCitZi"
        font.fontname = font.familyname + weight
        font.em = 1024
        hex_val = 0xe000
        hex_val_extend = 0xf0000
        outfile = dirname + weight + "/JyutcitziWith" + fontname + weight + ".ttf"

        has_oe = os.path.exists(char_folder+"oe.svg")
        vow_t = lambda v_char: 'oe' if has_oe and v_char == '居' else v_char
        cons_t = lambda c_char: '爻_tb' if c_char == '爻' else c_char

        def add_tones(target_prefix, hex_val_extend):
            for i, tone_char in enumerate(tonemarks):
                if record_mapping:
                    map_name = target_prefix.split("/")[-1]
                    ofile.write(hex(hex_val_extend)+' '+map_name+tone_char+'\n')
                add_glyph_to_font(font, hex_val_extend,
                                  target_prefix+str(i+1)+'.svg')

                hex_val_extend += 1
            return hex_val_extend

        # write hex values to file
        if record_mapping:
            ofile = open(record_loc, "w")
        # cons only
        for cons in consonants:
            assert hex_val < 0xf8ff
            if record_mapping:
                ofile.write(hex(hex_val)+" "+cons[1]+"`\n")
            add_glyph_to_font(font, hex_val,
                              block_folder+'only/cons/' + cons[1] + '`.svg')
            hex_val += 1
            # these can't have tones

        #ng
        # toneless
        if record_mapping:
            ofile.write(hex(hex_val)+' ng`\n')
        add_glyph_to_font(font, hex_val,
                          block_folder+'only/cons/ng`.svg')
        hex_val += 1
        # toneful
        hex_val_extend = add_tones(block_folder+'tones/only/cons/ng`', hex_val_extend)

        #m
        if record_mapping:
            ofile.write(hex(hex_val)+' m`\n')
        add_glyph_to_font(font, hex_val,
                          block_folder+'only/cons/m`.svg')
        hex_val += 1
        # toneful
        hex_val_extend = add_tones(block_folder+'tones/only/cons/m`', hex_val_extend)

        #ng_m
        ng_m_val = 0x20121 # compabtibility with glyphwiki
        if record_mapping:
            ofile.write(hex(hex_val)+' ng_m\n')
        add_glyph_to_font(font, ng_m_val,
                          char_folder+'ng.svg')
        # no one adds tones to this, since this character is reserved for 唔 m4/ng4

        # vowel only
        for vowel in vowels:
            assert hex_val < 0xf8ff
            if record_mapping:
                ofile.write(hex(hex_val)+" "+vowel[1]+"`\n")
            vow = vow_t(vowel[1])
            add_glyph_to_font(font, hex_val,
                              block_folder+'only/vows/' + vow + '`.svg')
            hex_val += 1
            hex_val_extend = add_tones(block_folder+'tones/only/vows/' + vow + '`', hex_val_extend)

        # cons + vowel
        for cons, vowel in itertools.product(consonants, vowels):
            assert hex_val < 0xf8ff
            if record_mapping:
                ofile.write(hex(hex_val)+' '+cons[1] + vowel[1]+'\n')
            vow = vow_t(vowel[1])
            add_glyph_to_font(font, hex_val,
                              block_folder+"cons_vows/" + cons[1] + vow +".svg")
            hex_val += 1
            hex_val_extend = add_tones(block_folder+"tones/cons_vows/" + cons[1] + vow, hex_val_extend)

        # cons + cons + vowel
        for cons, vowel in itertools.product(two_cons, vowels):
            assert hex_val < 0xf8ff
            if record_mapping:
                ofile.write(hex(hex_val)+' '+cons[1] + vowel[1]+'\n')
            vow = vow_t(vowel[1])
            add_glyph_to_font(font, hex_val,
                              block_folder+"two_cons_vows/" + cons[1] + vow +".svg")
            hex_val += 1
            hex_val_extend = add_tones(block_folder+"tones/two_cons_vows/" + cons[1] + vow, hex_val_extend)

        # cons + vowel + vowel
        assert hex_val < 0xf8ff
        if record_mapping:
            ofile.write(hex(hex_val)+' 厶乍乍\n')
        add_glyph_to_font(font, hex_val,
                         block_folder+ "cons_two_vows/厶乍乍.svg")
        hex_val += 1
        # no tone augmentation since 厶乍乍 corresponds uniquely to 卅


        # special characters
        for _, spec_char in spec_uni_particles + spec_uni_phrases + spec_uni_phrases_2:
            assert hex_val < 0xf8ff
            if record_mapping:
                ofile.write(hex(hex_val)+' '+spec_char+'\n')
            add_glyph_to_font(font, hex_val,
                              block_folder+"special_chars/combined/" +spec_char+".svg")
            hex_val += 1

        # 正_flip
        assert hex_val < 0xf8ff
        if record_mapping:
            ofile.write(hex(hex_val)+' 正_flip\n')
        add_glyph_to_font(font, hex_val,
                          char_folder+"正_flip.svg")
        hex_val += 1

        ## ======= second Version =========

        # more CCV (35*56) => 1960
        for two_con, vowel in itertools.product(two_cons_aug, vowels):
            assert hex_val < 0xf8ff
            if record_mapping:
                ofile.write(hex(hex_val)+' '+two_con[1] + vow_t(vowel[1])+'\n')
            add_glyph_to_font(font, hex_val,
                              block_folder+"two_cons_vows/" + two_con[1] + vow_t(vowel[1]) +".svg")
            hex_val += 1

        for two_con, vowel in itertools.product(two_cons_aug_toneful, vowels):
            hex_val_extend = add_tones(block_folder+"tones/two_cons_vows/" + two_con[1] + vow_t(vowel[1]), hex_val_extend)

        # (three_cons)V (10*56) => 616
        for conses, vowel in itertools.product(three_cons, vowels):
            assert hex_val < 0xf8ff
            chars = conses[1] + vow_t(vowel[1])
            if record_mapping:
                ofile.write(hex(hex_val)+' '+chars+'\n')
            add_glyph_to_font(font, hex_val,
                              block_folder+"three_cons_vow/"+chars+".svg")
            hex_val += 1
            # tone augmentation only for "shw"
            if conses == three_cons[-1]:
                hex_val_extend = add_tones(block_folder+"tones/three_cons_vow/"+chars, hex_val_extend)

        # VC + VS + VowSup => all VC 1176
        for cons, vowel in itertools.product(consonants, vowels):
            assert hex_val < 0xf8ff
            if record_mapping:
                ofile.write(hex(hex_val)+' '+vow_t(vowel[1]) + cons[1] + '\n')
            add_glyph_to_font(font, hex_val,
                              block_folder+"vows_cons/" + vow_t(vowel[1]) + cons[1] +".svg")
            hex_val += 1
            # no tone augmentation since VC must be from a loanword
            # e.g. ass (aas), ink (ingk)
            # hex_val_extend = add_tones(block_folder+"tones/vows_cons/" + vow_t(vowel[1]) + cons[1], hex_val_extend)

        # CC + CS + SupS + SupC => all CC (21*21) = 441
        for cons, cons2 in itertools.product(consonants, consonants):
            assert hex_val < 0xf8ff
            if record_mapping:
                ofile.write(hex(hex_val)+' '+cons[1] + cons2[1]+'\n')
            add_glyph_to_font(font, hex_val,
                              block_folder+"cons_cons/" + cons[1] + cons2[1] +".svg")
            hex_val += 1
            # consonant clusters generally cannot have tones
            # except for hng, since hng6 exists in Cantonese (addressed later)

        # cons + vowel + vowel
        assert hex_val < 0xf8ff
        if record_mapping:
            ofile.write(hex(hex_val)+' 厶丌乍\n')
        add_glyph_to_font(font, hex_val,
                          block_folder+"cons_two_vows/厶丌乍.svg")
        hex_val += 1
        # no tone augmentation since 厶丌乍 corresponds uniquely to 卅

        ### THIRD ITERATION
        #  艮, 亇, 止
        for vowel in ext_vows:
            assert hex_val < 0xf8ff
            if record_mapping:
                ofile.write(hex(hex_val)+" "+vowel[1]+"`\n")
            vow = vow_t(vowel[1])
            add_glyph_to_font(font, hex_val,
                              block_folder+'only/vows/' + vow + '`.svg')
            hex_val += 1
            hex_val_extend = add_tones(block_folder+'tones/only/vows/' + vow + '`', hex_val_extend)

        # [C w/ r,v]艮 + [C w/ r,v]亇 (v is optional here tbh)
        for cons, vowel in itertools.product(consonants+ext_cons, e_en):
            assert hex_val < 0xf8ff
            if record_mapping:
                ofile.write(hex(hex_val)+' '+cons[1] + vowel[1]+'\n')
            vow = vow_t(vowel[1])
            add_glyph_to_font(font, hex_val,
                              block_folder+"cons_vows/" + cons[1] + vow +".svg")
            hex_val += 1
            hex_val_extend = add_tones(block_folder+"tones/cons_vows/" + cons[1] + vow, hex_val_extend)

        # Cw艮
        for cons in consonants:
            assert hex_val < 0xf8ff
            if record_mapping:
                ofile.write(hex(hex_val)+' '+cons[1] + '禾艮\n')
            temp = cons_t(cons[1])
            add_glyph_to_font(font, hex_val,
                              block_folder+"two_cons_vows/" + cons[1] +"禾艮.svg")
            hex_val += 1
            hex_val_extend = add_tones(block_folder+"tones/two_cons_vows/" + cons[1] +"禾艮", hex_val_extend)

        # r, v
        for cons, vowel in itertools.product(ext_cons, vowels):
            assert hex_val < 0xf8ff
            if record_mapping:
                ofile.write(hex(hex_val)+' '+cons[1] + vowel[1]+'\n')
            vow = vow_t(vowel[1])
            add_glyph_to_font(font, hex_val,
                              block_folder+"cons_vows/" + cons[1] + vow +".svg")
            hex_val += 1
            hex_val_extend = add_tones(block_folder+"tones/cons_vows/" + cons[1] + vow, hex_val_extend)

        # [zh, ch, sh, r] x z
        # Note: zz, cz, sz are already covered in CC
        for cons in zcs:
            assert hex_val < 0xf8ff
            if record_mapping:
                ofile.write(hex(hex_val)+' '+cons[1] + '亾止\n')
            add_glyph_to_font(font, hex_val,
                              block_folder+"two_cons_vows/" + cons[1] +"亾止.svg")
            hex_val += 1
            hex_val_extend = add_tones(block_folder+"tones/two_cons_vows/" + cons[1] +"亾止", hex_val_extend)

            hex_val_extend = add_tones(block_folder+"tones/cons_cons/" + cons[1] +"止", hex_val_extend)

        assert hex_val < 0xf8ff
        if record_mapping:
            ofile.write(hex(hex_val)+' ㄖ止\n')
        add_glyph_to_font(font, hex_val, block_folder+"cons_vows/ㄖ止.svg")
        hex_val += 1
        hex_val_extend = add_tones(block_folder+"tones/cons_vows/ㄖ止", hex_val_extend)

        ### CONSONANT CLUSTERS
        # [mw, lw, rw, hj, nj, lj, ngj, zh, ch, wl] x V
        for two_con, vowel in itertools.product(two_cons_aug2, vowels):
            assert hex_val < 0xf8ff
            if record_mapping:
                ofile.write(hex(hex_val)+' '+two_con[1] + vow_t(vowel[1])+'\n')
            add_glyph_to_font(font, hex_val,
                              block_folder+"two_cons_vows/" + two_con[1] + vow_t(vowel[1]) +".svg")
            hex_val += 1
            hex_val_extend = add_tones(block_folder+"tones/two_cons_vows/" + two_con[1] + vow_t(vowel[1]), hex_val_extend)

        # hex_val is filled at this point, add to hex_val_extend instead
        # zhw, chw
        for conses, vowel in itertools.product(three_cons_2, vowels):
            assert hex_val_extend < 0xffffd
            chars = conses[1] + vow_t(vowel[1])
            if record_mapping:
                ofile.write(hex(hex_val)+' '+chars+'\n')
            add_glyph_to_font(font, hex_val_extend,
                              block_folder+"three_cons_vow/"+chars+".svg")
            hex_val_extend += 1
            hex_val_extend = add_tones(block_folder+"tones/three_cons_vow/" + chars, hex_val_extend)
        # [j, n, l, z, c, s] x yue
        # [l, z, c, s] x yuen
        for conses, ending in [(cons_yue, "仒旡"), (cons_yuen, "仒円")]:
            for cons in conses:
                assert hex_val_extend < 0xffffd
                chars = cons[1] + ending
                if record_mapping:
                    ofile.write(hex(hex_val_extend)+' '+chars+'\n')
                add_glyph_to_font(font, hex_val_extend,
                                  block_folder+"cons_two_vows/"+chars+".svg")
                hex_val_extend += 1
                hex_val_extend = add_tones(block_folder+"tones/cons_two_vows/" + chars, hex_val_extend)

        # add toneful repeat marks
        hex_val_extend = add_tones(block_folder+'tones/repeat_mark/々', hex_val_extend)

        # add toneful hng (since hng6 exists in HK Cantonese)
        hex_val_extend = add_tones(block_folder+"tones/cons_cons/亾爻", hex_val_extend)

        ### generate the file
        font.autoWidth(150)
        font.generate(outfile)
        print("generated",outfile)
        font.close()

        if record_mapping:
            ofile.close()
            record_mapping = False
