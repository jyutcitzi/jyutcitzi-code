import itertools
import svgutils
import sys
import os
from chars import *
from fonts_config import fontdirs
from tone_settings import consts, add_tone

def glyph_fromfile(file, size=1000):
    fig = svgutils.transform.fromfile(file)
    if fig.height is not None and fig.width is not None:
        plot = fig.getroot()
        plot.scale_xy(size/int(fig.width), size/int(fig.height))
        temp = svgutils.transform.SVGFigure(size, size)
        temp.append([plot])
        fig = temp
        pass
    elif fig.height is None and fig.width is None:
        fig.height, fig.width = size, size# 1010
    else:
        raise NotImplementedError
    return fig

# def rescale_fig(src_fig, tgt_fig):
#     plot2 = tgt_fig.getroot()
#     plot2.scale_xy(int(src_fig.width)/int(tgt_fig.width)*1.0,
#                    int(src_fig.height)/int(tgt_fig.height)*1.0)
#     temp = svgutils.transform.SVGFigure(src_fig.width, src_fig.height)
#     temp.append([plot2])
#     return temp

def merge_two(left_loc, right_loc, mode, offset=5):
    assert mode in ['tb', 'lr']
    fig1 = glyph_fromfile(left_loc)
    fig2 = glyph_fromfile(right_loc)
    # for loc in [left_loc, right_loc]:
    #     if '爻_tb.svg' in loc or 'oe.svg' in loc or 'ng.svg' in loc:
    #         if loc == left_loc:
    #             fig1 = rescale_fig(fig2, fig1)
    #         elif loc == right_loc:
    #             fig2 = rescale_fig(fig1, fig2)
    assert fig1.width == fig2.width and fig1.height == fig2.height
    fig = svgutils.transform.SVGFigure(fig1.width, fig1.height)

    plot1, plot2 = fig1.getroot(), fig2.getroot()
    if mode == 'lr':
        if left_loc[-5:-4] == '口':
            plot1.scale_xy(1./3,1)
            plot2.scale_xy(2./3,1)
            plot2.moveto(int(fig1.width)/3 - offset, 0)
        elif left_loc[-5:-4] in ['忄','扌']:
            plot1.scale_xy(0.5,1)
            plot2.scale_xy(0.6,1)
            plot2.moveto(int(fig1.width)* 0.4 - offset, 0)
        else:
            plot1.scale_xy(0.5,1)
            plot2.scale_xy(0.5,1)
            plot2.moveto(int(fig1.width)/2 - offset, 0)
        plot1.moveto(offset, 0)
    else:
        plot1.scale_xy(1,0.5)
        plot2.scale_xy(1,0.5)
        plot1.moveto(0, offset)
        plot2.moveto(0, int(fig1.width)/2 - offset)

    fig.append([plot1, plot2])
    return fig

def merge_three(first, second, third, mode, offset=5):
    assert mode in ['tbr', 'lrb']
    fig1 = glyph_fromfile(first)
    fig2 = glyph_fromfile(second)
    fig3 = glyph_fromfile(third)
    # for loc in [first, second, third]:
    #     if 'oe.svg' in loc or '爻_tb.svg' in loc:
    #         if loc == first:
    #             fig1 = rescale_fig(fig2, fig1)
    #         elif loc == second:
    #             fig2 = rescale_fig(fig3, fig2)
    #         elif loc == third:
    #             fig3 = rescale_fig(fig1, fig3)
    assert fig1.width == fig2.width and fig2.width == fig3.width \
     and fig1.height == fig2.height and fig2.height == fig3.height
    fig = svgutils.transform.SVGFigure(fig1.width, fig1.height)
    plot1, plot2, plot3 = fig1.getroot(), fig2.getroot(), fig3.getroot()
    if mode == 'lrb':
        plot1.scale_xy(0.5,0.5)
        plot2.scale_xy(0.5,0.5)
        plot3.scale_xy(1, 0.5)
        plot1.moveto(offset, offset)
        plot2.moveto(int(fig1.width)/2 - offset, offset)
        plot3.moveto(0, int(fig1.width)/2 - offset)
    else:
        plot1.scale_xy(0.5,0.5)
        plot2.scale_xy(0.5,0.5)
        plot3.scale_xy(0.5, 1)
        plot1.moveto(offset, offset)
        plot2.moveto(offset, int(fig1.width)/2 - offset)
        plot3.moveto(int(fig1.width)/2 - offset, 0)
    fig.append([plot1, plot2, plot3])
    return fig

def merge_three_cons_vow(first, second, third, vow, offset=5):
    fig1 = glyph_fromfile(first)
    fig2 = glyph_fromfile(second)
    fig3 = glyph_fromfile(third)
    fig4 = glyph_fromfile(vow)
    # for loc in [first, second, third, vow]:
    #     if 'oe.svg' in loc or '爻_tb.svg' in loc:
    #         if loc == first:
    #             fig1 = rescale_fig(fig2, fig1)
    #         elif loc == second:
    #             fig2 = rescale_fig(fig3, fig2)
    #         elif loc == third:
    #             fig3 = rescale_fig(fig1, fig3)
    #         elif loc == vow:
    #             fig4 = rescale_fig(fig1, fig4)
    assert fig1.width == fig2.width and \
            fig2.width == fig3.width and \
            fig3.width == fig4.width and \
            fig1.height == fig2.height and \
            fig2.height == fig3.height and \
            fig3.width == fig4.width
    fig = svgutils.transform.SVGFigure(fig1.width, fig1.height)

    plot1, plot2 = fig1.getroot(), fig2.getroot()
    plot3, plot4 = fig3.getroot(), fig4.getroot()
    plot1.scale_xy(0.5,1.0/3)
    plot2.scale_xy(0.5,1.0/3)
    plot3.scale_xy(0.5,1.0/3)
    plot4.scale_xy(0.5, 1)

    plot1.moveto(offset, offset)
    plot2.moveto(offset, int(fig1.width)/3.0)
    plot3.moveto(offset, int(fig1.width)/3.0 * 2 - offset)
    plot4.moveto(int(fig1.width)/2 - offset, 0)

    fig.append([plot1, plot2, plot3, plot4])
    return fig

def make_if_not_exist(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

for fontdir in fontdirs:
    # folder where components are stored at
    char_folder = fontdir + 'chars/'
    block_folder = fontdir + 'blocks/'

    # make the folders
    # make_if_not_exist('./fonts/PMingLiu/blocks/')
    for folder in ['cons_cons','vows_cons','three_cons_vow','special_chars/combined', 'cons_two_vows', 'two_cons_vows', 'cons_vows', 'only/vows', 'only/cons']:
        make_if_not_exist(block_folder+folder)

    three_dot_file = char_folder+"𭕄.svg" if os.path.exists(char_folder+"𭕄.svg") else "./orig_chars/only/three_dots.svg"
    tl_dot_file = char_folder+"top_left_dot.svg" if os.path.exists(char_folder+"top_left_dot.svg") else "./orig_chars/top_left_dot.svg"
    L_file = char_folder+'辶.svg' if os.path.exists(char_folder+'辶.svg') else './orig_chars/special_chars/parts/辶.svg'

    has_oe = os.path.exists(char_folder+"oe.svg")
    vow_t = lambda v_char: 'oe' if has_oe and v_char == '居' else v_char
    cons_t = lambda c_char: '爻_tb' if c_char == '爻' else c_char

    def add_three_dots(loc, three_dot_file=three_dot_file,
                       frac=0.7):
        fig1 = glyph_fromfile(three_dot_file)
        fig2 = glyph_fromfile(loc)
        fig = svgutils.transform.SVGFigure(fig1.width, fig1.height)
        plot1 = fig1.getroot()
        plot2 = fig2.getroot()
        plot2.scale_xy(1.0, frac)
        plot2.moveto(0, float(fig1.width)*(1-frac))
        if 'SourceHan' in three_dot_file:
            plot1.scale_xy(1.0, 0.6)
        fig.append([plot1, plot2])
        return fig


    def dot(loc, dot_file=tl_dot_file,
            frac=0.9, mode="top"):
        fig1 = glyph_fromfile(dot_file)
        fig2 = glyph_fromfile(loc)
        fig = svgutils.transform.SVGFigure(fig2.width, fig2.height)
        plot1 = fig1.getroot()
        plot1.scale_xy(int(fig2.width)/int(fig1.width),int(fig2.height)/int(fig1.height))
        if mode == 'bottom':
            plot1.moveto(0, int(fig2.width)*0.7)

        plot2 = fig2.getroot()
        plot2.scale_xy(frac, frac)
        plot2.moveto(0, int(fig2.width)*(1-frac))
        fig.append([plot1, plot2])
        return fig


    def L(loc, Lfile=L_file):
        fig1 = glyph_fromfile(Lfile)
        fig2 = glyph_fromfile(loc)
        assert fig1.width == fig2.width and \
                fig1.height == fig2.height
        fig = svgutils.transform.SVGFigure(fig1.width, fig1.height)
        plot = fig2.getroot()
        plot.scale_xy(0.5, 0.85)
        plot.moveto(0.375*int(fig1.width), 0) # 75
        fig.append([fig1.getroot(), plot])
        return fig

    def augment_tones(block_folder, svg_file_no_suffix, fontdir):
        temp = block_folder+'tones/'+svg_file_no_suffix
        # make_if_not_exist("/".join(temp.split("/")[:-1]))
        for tone in range(1,9):
            fig = add_tone(block_folder+svg_file_no_suffix+'.svg', fontdir, tone)
            fig.save(block_folder+'tones/'+svg_file_no_suffix+str(tone)+'.svg')

    # create 正_flip
    if not os.path.exists(char_folder + '正_flip.svg'):
        fig = glyph_fromfile(char_folder + '正.svg')
        plot = fig.getroot()
        plot.scale_xy(-1,1)
        plot.moveto(int(fig.width),0)
        fig.append([plot])
        fig.save(char_folder + '正_flip.svg')

    # create 爻_tb
    if not os.path.exists(char_folder + '爻_tb.svg'):
        fig1 = glyph_fromfile(char_folder + '乂.svg')
        fig2 = glyph_fromfile(char_folder + '乂.svg')
        fig = svgutils.transform.SVGFigure(fig1.width, fig1.height)
        plot1, plot2 = fig1.getroot(), fig2.getroot()
        plot1.scale_xy(0.5,1)
        plot2.scale_xy(0.5,1)
        plot2.moveto(int(fig1.width)/2,0)
        fig.append([plot1, plot2])
        fig.save(char_folder + '爻_tb.svg')

    #phonetics
    # cons only
    # it's not possible for these to have tones
    for cons in consonants:
        fig = add_three_dots(char_folder + cons[1] + '.svg')
        fig.save(block_folder+'only/cons/' + cons[1] + '`.svg')

    #ng
    fig = dot(char_folder+'ng.svg', mode='top')
    fig.save(block_folder+'only/cons/ng`.svg')
    augment_tones(block_folder, 'only/cons/ng`', fontdir)

    #m
    fig = dot(char_folder+'ng.svg', mode='bottom')
    fig.save(block_folder+'only/cons/m`.svg')
    augment_tones(block_folder, 'only/cons/m`', fontdir)

    # vows only
    for vowel in vowels:
        vow = vow_t(vowel[1])
        fig = add_three_dots(char_folder + vow + '.svg')
        fig.save(block_folder+'only/vows/' + vow + '`.svg')
        augment_tones(block_folder, 'only/vows/' + vow + '`', fontdir)

    # cons + vows (21*56) = 1176
    for cons, vowel in itertools.product(consonants, vowels):
        temp = cons_t(cons[1])
        vow = vow_t(vowel[1])
        fig = merge_two(char_folder + temp + '.svg',
                        char_folder + vow + '.svg',
                        'lr' if cons[2] == '⿰' else 'tb')
        fig.save(block_folder+"cons_vows/" + cons[1] + vow +".svg")
        augment_tones(block_folder, "cons_vows/" + cons[1] + vow, fontdir)

    # two_cons + vows (10*56) = 560
    for two_con, vowel in itertools.product(two_cons, vowels):
        vow = vow_t(vowel[1])
        fig = merge_three(char_folder + two_con[1][0] + '.svg',
                          char_folder + two_con[1][1] + '.svg',
                          char_folder + vow + '.svg', 'tbr')
        fig.save(block_folder+"two_cons_vows/" + two_con[1] + vow +".svg")
        augment_tones(block_folder, "two_cons_vows/" + two_con[1] + vow, fontdir)

    # cons + two_vows (saaa for now)
    fig = merge_three(char_folder + '厶.svg',
                      char_folder + '乍.svg',
                      char_folder + '乍.svg', 'tbr')
    fig.save(block_folder + "cons_two_vows/厶乍乍.svg")
    # no tone augmentation since 厶乍乍 corresponds uniquely to 卅
    # augment_tones(block_folder, "cons_two_vows/厶乍乍", fontdir)

    # repeat mark 々 with tone marks
    make_if_not_exist(block_folder+'tones/repeat_mark')
    for tone in range(1,9):
        fig = add_tone(char_folder + '々.svg', fontdir, tone)
        fig.save(block_folder+'tones/repeat_mark/々'+str(tone)+'.svg')

    # special characters
    fig = merge_two(char_folder + '彳.svg',
                    char_folder + '固.svg', 'lr', offset=15)
    fig.save(block_folder + 'special_chars/combined/彳固.svg')

    fig = merge_two(char_folder + '少.svg',
                    char_folder + '々.svg', 'tb')
    fig.save(block_folder + 'special_chars/combined/少々.svg')

    fig = merge_two(char_folder + 'ng.svg',
                    char_folder + '係.svg', 'tb')
    fig.save(block_folder + 'special_chars/combined/ng係.svg')

    fig = merge_two(char_folder + '工.svg',
                    char_folder + '耳.svg', 'tb')
    fig.save(block_folder + 'special_chars/combined/工耳.svg')

    fig = merge_two(char_folder + '彳.svg',
                    char_folder + '糸.svg', 'lr', offset=15)
    fig.save(block_folder + 'special_chars/combined/彳糸.svg')

    fig = merge_two(char_folder + '正.svg',
                    char_folder + '岩.svg', 'lr')
    fig.save(block_folder + 'special_chars/combined/正岩.svg')

    fig = merge_two(char_folder + '自.svg',
                    char_folder + '由.svg', 'tb')
    fig.save(block_folder + 'special_chars/combined/自由.svg')

    for radical in ['忄', '黹']:
        for cv in ['禾子','厶云']:
            fig = merge_two(char_folder+radical+'.svg',
                            block_folder+'cons_vows/'+cv+'.svg', 'lr')
            fig.save(block_folder+'special_chars/combined/'+radical+cv+'.svg')

    for part in ['兒','臣']:
        fig = merge_two(char_folder + '黹.svg',
                        char_folder + part+'.svg', 'lr')
        fig.save(block_folder+'special_chars/combined/黹'+part+'.svg')

    fig = merge_two(block_folder+'only/vows/乍`.svg',
                    char_folder+'戈.svg', 'lr')
    fig.save(block_folder + 'special_chars/combined/乍`戈.svg')

    fig = merge_two(block_folder +'cons_vows/天尺.svg',
                    char_folder+'戈.svg', 'lr')
    fig.save(block_folder+'special_chars/combined/天尺戈.svg')

    fig = merge_two(char_folder+'口.svg',
                    block_folder+'only/vows/勺`.svg', 'lr')
    fig.save(block_folder+'special_chars/combined/口勺`.svg')

    fig = merge_two(char_folder+'忄.svg',
                    block_folder+'cons_vows/夫么.svg', 'lr')
    fig.save(block_folder+'special_chars/combined/忄夫么.svg')

    fig = merge_two(char_folder+'扌.svg',
                    block_folder+'cons_vows/爻丂.svg', 'lr')
    fig.save(block_folder+'special_chars/combined/扌爻丂.svg')

    fig = L(block_folder+'cons_vows/厶円.svg')
    fig.save(block_folder+'special_chars/combined/辶厶円.svg')

    # cons + vows + vows (21*56*56) = 65,856 (add in future)

    # ===========================
    # SECOND ITERATION
    # ===========================
    # (two_cons_aug)V
    cons_loc = lambda c_char: char_folder + cons_t(c_char) + '.svg'
    vow_loc = lambda v_char: char_folder + vow_t(v_char) + '.svg'

    # more CCV
    for two_con, vowel in itertools.product(two_cons_aug, vowels):
        fig = merge_three(cons_loc(two_con[1][0]),
                          cons_loc(two_con[1][1]),
                          vow_loc(vowel[1]), 'tbr')
        fig.save(block_folder+"two_cons_vows/" + two_con[1] + vow_t(vowel[1]) +".svg")
        augment_tones(block_folder, "two_cons_vows/" + two_con[1] + vow_t(vowel[1]), fontdir)


    # (three_cons)V (10*56) => 616
    for conses, vowel in itertools.product(three_cons, vowels):
        chars = conses[1] + vow_t(vowel[1])
        fig = merge_three_cons_vow(cons_loc(conses[1][0]), cons_loc(conses[1][1]), cons_loc(conses[1][2]), vow_loc(vowel[1]))
        fig.save(block_folder+"three_cons_vow/"+chars+".svg")
        augment_tones(block_folder, "three_cons_vow/"+chars, fontdir)

    # VC + VS + VowSup => all VC 1176
    for cons, vowel in itertools.product(consonants, vowels):
        fig = merge_two(vow_loc(vowel[1]),
                        cons_loc(cons[1]),
                        'lr' if cons[2] == '⿰' else 'tb')
        fig.save(block_folder+"vows_cons/" + vow_t(vowel[1]) + cons[1] +".svg")
        augment_tones(block_folder, "vows_cons/" + vow_t(vowel[1]) + cons[1], fontdir)

    # CC + CS + SupS + SupC => all CC (21*21) = 441
    # generally cannot have tones since it only has consonants, but files created anyways in case it is useful in the future
    # e.g. tone-ful Cz is useful for mandarin tones
    # note: toneful hng exists (e.g. hng6) exists in HK Cantonese
    for cons, cons2 in itertools.product(consonants, consonants):
        if cons[2] == '⿰':
            fig = merge_two(cons_loc(cons[1]),
                            char_folder + cons2[1] + '.svg',
                            'lr')
        else:
            fig = merge_two(cons_loc(cons[1]),
                            cons_loc(cons2[1]),
                            'tb')
        fig.save(block_folder+"cons_cons/" + cons[1] + cons2[1] +".svg")
        augment_tones(block_folder, "cons_cons/" + cons[1] + cons2[1], fontdir)

    # cons + two_vows (seiaa too)
    fig = merge_three(cons_loc('厶'),
                      vow_loc('丌'),
                      vow_loc('乍'), 'tbr')
    fig.save(block_folder+"cons_two_vows/厶丌乍.svg")
    # no tone augmentation since 厶丌乍 corresponds uniquely to 卌
    # augment_tones(block_folder, "cons_two_vows/厶丌乍", fontdir)

    # =======================
    # THIRD ITERATION
    # =======================
    # TODO: can combine code below with code above, since the order for generating the SVG files do not matter
    ### EXTENDED COMPONENTS
    # 艮, 亇, 止
    for vowel in ext_vows:
        fig = add_three_dots(char_folder + vowel[1] + '.svg')
        fig.save(block_folder+'only/vows/' + vowel[1] + '`.svg')
        augment_tones(block_folder, 'only/vows/' + vowel[1] + '`', fontdir)

    # [C w/ r,v]艮 + [C w/ r,v]亇 (v is optional here tbh)
    for cons, vowel in itertools.product(consonants+ext_cons, e_en):
        temp = cons_t(cons[1])
        vow = vow_t(vowel[1])
        fig = merge_two(cons_loc(temp), vow_loc(vow),
                        'lr' if cons[2] == '⿰' else 'tb')
        fig.save(block_folder+"cons_vows/" + cons[1] + vow +".svg")
        augment_tones(block_folder, "cons_vows/" + cons[1] + vow, fontdir)


    # Cw艮
    for cons in consonants:
        temp = cons_t(cons[1])
        fig = merge_three(cons_loc(temp), cons_loc('禾'), vow_loc('艮'), 'tbr')
        fig.save(block_folder+"two_cons_vows/" + cons[1] + "禾艮.svg")
        augment_tones(block_folder, "two_cons_vows/" + cons[1] + "禾艮", fontdir)

    # r, v
    for cons, vowel in itertools.product(ext_cons, vowels):
        temp = cons_t(cons[1])
        vow = vow_t(vowel[1])
        fig = merge_two(cons_loc(temp), vow_loc(vow),
                        'lr' if cons[2] == '⿰' else 'tb')
        fig.save(block_folder+"cons_vows/" + cons[1] + vow +".svg")
        augment_tones(block_folder, "cons_vows/" + cons[1] + vow, fontdir)

    # [zh, ch, sh, r] x z
    # Note: zz, cz, sz (no tones and toneful) are already covered in CC
    for cons in zcs:
        fig = merge_three(cons_loc(cons[1]), cons_loc('亾'), cons_loc('止'), 'tbr')
        fig.save(block_folder+"two_cons_vows/" + cons[1] + "亾止.svg")
        augment_tones(block_folder, "two_cons_vows/" + cons[1] + "亾止", fontdir)

    fig = merge_two(cons_loc('ㄖ'), cons_loc('止'), 'lr')
    fig.save(block_folder+"cons_vows/ㄖ止.svg")
    augment_tones(block_folder, "cons_vows/ㄖ止", fontdir)


    ### CONSONANT CLUSTERS
    # [mw, lw, rw, hj, nj, lj, ngj, zh, ch] x V
    for two_con, vowel in itertools.product(two_cons_aug2, vowels):
        fig = merge_three(cons_loc(two_con[1][0]),
                          cons_loc(two_con[1][1]),
                          vow_loc(vowel[1]), 'tbr')
        fig.save(block_folder+"two_cons_vows/" + two_con[1] + vow_t(vowel[1]) +".svg")
        augment_tones(block_folder, "two_cons_vows/" + two_con[1] + vow_t(vowel[1]), fontdir)
    # zhw, chw
    for conses, vowel in itertools.product(three_cons_2, vowels):
        chars = conses[1] + vow_t(vowel[1])
        fig = merge_three_cons_vow(cons_loc(conses[1][0]), cons_loc(conses[1][1]), cons_loc(conses[1][2]), vow_loc(vowel[1]))
        fig.save(block_folder+"three_cons_vow/" + chars + ".svg")
        augment_tones(block_folder, "three_cons_vow/" + chars, fontdir)
    # [j, n, l, z, c, s] x yue
    for cons in cons_yue:
        temp = cons_t(cons[1])
        fig = merge_three(cons_loc(cons[1]), cons_loc('仒'), cons_loc('旡'),
                          'lrb' if cons[2] == '⿰' else 'tbr')
        fig.save(block_folder+"cons_two_vows/" + temp + "仒旡.svg")
        augment_tones(block_folder, "cons_two_vows/" + temp + "仒旡", fontdir)
    # [j, l, z, c, s] x yuen
    for cons in cons_yuen:
        temp = cons_t(cons[1])
        fig = merge_three(cons_loc(cons[1]), cons_loc('仒'), cons_loc('円'),
                         'lrb' if cons[2] == '⿰' else 'tbr')
        fig.save(block_folder+"cons_two_vows/" + temp + "仒円.svg")
        augment_tones(block_folder, "cons_two_vows/" + temp + "仒円", fontdir)

    # Note: [z, c, s] x 止 x [m, n, p, t] is handled by the RIME keyboard
