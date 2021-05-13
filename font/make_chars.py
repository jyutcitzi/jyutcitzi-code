import itertools
import svgutils
import sys
from chars import *

def add_three_dots(loc, three_dot_file="./font/orig_chars/only/three_dots.svg",
                   frac=0.7):
    fig1 = svgutils.transform.fromfile(three_dot_file)
    fig2 = svgutils.transform.fromfile(loc)
    fig = svgutils.transform.SVGFigure(fig1.width, fig1.height)
    plot1 = fig1.getroot()
    plot2 = fig2.getroot()
    plot2.scale_xy(1.0, frac)
    plot2.moveto(0, float(fig1.width)*(1-frac))
    fig.append([plot1, plot2])
    return fig


def dot(loc, dot_file="./font/orig_chars/top_left_dot.svg",
        frac=0.9, mode="top"):
    fig1 = svgutils.transform.fromfile(dot_file)
    fig2 = svgutils.transform.fromfile(loc)
    fig = svgutils.transform.SVGFigure(fig1.width, fig1.height)
    plot1 = fig1.getroot()
    if mode == 'bottom':
        plot1.moveto(0, fig1.width*0.7)

    plot2 = fig2.getroot()
    plot2.scale_xy(frac, frac)
    plot2.moveto(0, fig1.width*(1-frac))
    fig.append([plot1, plot2])
    return fig


def L(loc, Lfile='./font/orig_chars/special_chars/parts/辶.svg'):
    fig1 = svgutils.transform.fromfile(Lfile)
    fig2 = svgutils.transform.fromfile(loc)
    fig = svgutils.transform.SVGFigure(fig1.width, fig1.height)
    plot = fig2.getroot()
    plot.scale_xy(0.5, 0.85)
    plot.moveto(0.375*fig1.width, 0) # 75
    fig.append([fig1.getroot(), plot])
    return fig

def merge_two(left_loc, right_loc, mode, offset=5):
    assert mode in ['tb', 'lr']
    fig1 = svgutils.transform.fromfile(left_loc)
    fig2 = svgutils.transform.fromfile(right_loc)
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
    fig1 = svgutils.transform.fromfile(first)
    fig2 = svgutils.transform.fromfile(second)
    fig3 = svgutils.transform.fromfile(third)
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
    fig1 = svgutils.transform.fromfile(first)
    fig2 = svgutils.transform.fromfile(second)
    fig3 = svgutils.transform.fromfile(third)
    fig4 = svgutils.transform.fromfile(vow)
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

# cons only
for cons in consonants:
    fig = add_three_dots('./font/orig_chars/cons/' + cons[1] + '.svg')
    fig.save('./font/orig_chars/only/cons/' + cons[1] + '`.svg')

#ng
fig = dot('./font/orig_chars/cons/ng.svg', mode='top')
fig.save('./font/orig_chars/only/cons/ng`.svg')
#m
fig = dot('./font/orig_chars/cons/ng.svg', mode='bottom')
fig.save('./font/orig_chars/only/cons/m`.svg')

# vows only
for vowel in vowels:
    vow = 'oe' if vowel[1] == '居' else vowel[1]
    fig = add_three_dots('./font/orig_chars/vows/' + vow + '.svg')
    fig.save('./font/orig_chars/only/vows/' + vow + '`.svg')

# cons + vows (21*56) = 1176
for cons, vowel in itertools.product(consonants, vowels):
    temp = '爻_tb' if cons[1] == '爻' else cons[1]
    vow = 'oe' if vowel[1] == '居' else vowel[1]
    fig = merge_two('./font/orig_chars/cons/' + temp + '.svg',
                    './font/orig_chars/vows/' + vow + '.svg',
                    'lr' if cons[2] == '⿰' else 'tb')
    fig.save("./font/orig_chars/cons_vows/" + cons[1] + vow +".svg")

# two_cons + vows (10*56) = 560
for two_con, vowel in itertools.product(two_cons, vowels):
    vow = 'oe' if vowel[1] == '居' else vowel[1]
    fig = merge_three('./font/orig_chars/cons/' + two_con[1][0] + '.svg',
                      './font/orig_chars/cons/' + two_con[1][1] + '.svg',
                      './font/orig_chars/vows/' + vow + '.svg', 'tbr')
    fig.save("./font/orig_chars/two_cons_vows/" + two_con[1] + vow +".svg")

# cons + two_vows (saaa for now)
fig = merge_three('./font/orig_chars/cons/厶.svg',
                  './font/orig_chars/vows/乍.svg',
                  './font/orig_chars/vows/乍.svg', 'tbr')
fig.save("./font/orig_chars/cons_two_vows/厶乍乍.svg")

# special characters
fig = merge_two('./font/orig_chars/special_chars/parts/彳.svg',
                './font/orig_chars/special_chars/parts/固.svg', 'lr', offset=15)
fig.save('./font/orig_chars/special_chars/combined/彳固.svg')

fig = merge_two('./font/orig_chars/special_chars/parts/少.svg',
                './font/orig_chars/special_chars/parts/々.svg', 'tb')
fig.save('./font/orig_chars/special_chars/combined/少々.svg')

fig = merge_two('./font/orig_chars/cons/ng.svg',
                './font/orig_chars/special_chars/parts/係.svg', 'tb')
fig.save('./font/orig_chars/special_chars/combined/ng係.svg')

fig = merge_two('./font/orig_chars/vows/工.svg',
                './font/orig_chars/special_chars/parts/耳.svg', 'tb')
fig.save('./font/orig_chars/special_chars/combined/工耳.svg')

fig = merge_two('./font/orig_chars/special_chars/parts/彳.svg',
                './font/orig_chars/special_chars/parts/糸.svg', 'lr', offset=15)
fig.save('./font/orig_chars/special_chars/combined/彳糸.svg')

fig = merge_two('./font/orig_chars/special_chars/parts/正.svg',
                './font/orig_chars/special_chars/parts/岩.svg', 'lr')
fig.save('./font/orig_chars/special_chars/combined/正岩.svg')

fig = merge_two('./font/orig_chars/special_chars/parts/自.svg',
                './font/orig_chars/special_chars/parts/由.svg', 'tb')
fig.save('./font/orig_chars/special_chars/combined/自由.svg')

for radical in ['忄', '黹']:
    for cv in ['禾子','厶云']:
        fig = merge_two('./font/orig_chars/special_chars/parts/'+radical+'.svg',
                        './font/orig_chars/cons_vows/'+cv+'.svg', 'lr')
        fig.save('./font/orig_chars/special_chars/combined/'+radical+cv+'.svg')

for part in ['兒','臣']:
    fig = merge_two('./font/orig_chars/special_chars/parts/黹.svg',
                    './font/orig_chars/special_chars/parts/'+part+'.svg', 'lr')
    fig.save('./font/orig_chars/special_chars/combined/黹'+part+'.svg')

fig = merge_two('./font/orig_chars/only/vows/乍`.svg',
                './font/orig_chars/special_chars/parts/戈.svg', 'lr')
fig.save('./font/orig_chars/special_chars/combined/乍`戈.svg')

fig = merge_two('./font/orig_chars/cons_vows/天尺.svg',
                './font/orig_chars/special_chars/parts/戈.svg', 'lr')
fig.save('./font/orig_chars/special_chars/combined/天尺戈.svg')

fig = merge_two('./font/orig_chars/special_chars/parts/口.svg',
                './font/orig_chars/only/vows/勺`.svg', 'lr')
fig.save('./font/orig_chars/special_chars/combined/口勺`.svg')

fig = merge_two('./font/orig_chars/special_chars/parts/忄.svg',
                './font/orig_chars/cons_vows/夫么.svg', 'lr')
fig.save('./font/orig_chars/special_chars/combined/忄夫么.svg')

fig = merge_two('./font/orig_chars/special_chars/parts/扌.svg',
                './font/orig_chars/cons_vows/爻丂.svg', 'lr')
fig.save('./font/orig_chars/special_chars/combined/扌爻丂.svg')

fig = L('./font/orig_chars/cons_vows/厶円.svg')
fig.save('./font/orig_chars/special_chars/combined/辶厶円.svg')

# cons + vows + vows (21*56*56) = 65,856 (add in future)

# ===========================
# SECOND ITERATION
# ===========================
# (two_cons_aug)V
vow_t = lambda v_char: 'oe' if v_char == '居' else v_char
cons_t = lambda c_char: '爻_tb' if c_char == '爻' else c_char
cons_loc = lambda c_char: './font/orig_chars/cons/' + cons_t(c_char) + '.svg'
vow_loc = lambda v_char: './font/orig_chars/vows/' + vow_t(v_char) + '.svg'

# more CCV
for two_con, vowel in itertools.product(two_cons_aug, vowels):
    fig = merge_three(cons_loc(two_con[1][0]),
                      cons_loc(two_con[1][1]),
                      vow_loc(vowel[1]), 'tbr')
    fig.save("./font/orig_chars/two_cons_vows/" + two_con[1] + vow_t(vowel[1]) +".svg")

# (three_cons)V (10*56) => 616
for conses, vowel in itertools.product(three_cons, vowels):
    chars = conses[1] + vow_t(vowel[1])
    fig = merge_three_cons_vow(cons_loc(conses[1][0]), cons_loc(conses[1][1]), cons_loc(conses[1][2]), vow_loc(vowel[1]))
    fig.save("./font/orig_chars/three_cons_vow/"+chars+".svg")

# VC + VS + VowSup => all VC 1176
for cons, vowel in itertools.product(consonants, vowels):
    fig = merge_two(vow_loc(vowel[1]),
                    cons_loc(cons[1]),
                    'lr' if cons[2] == '⿰' else 'tb')
    fig.save("./font/orig_chars/vows_cons/" + vow_t(vowel[1]) + cons[1] +".svg")

# CC + CS + SupS + SupC => all CC (21*21) = 441
for cons, cons2 in itertools.product(consonants, consonants):
    if cons[2] == '⿰':
        fig = merge_two(cons_loc(cons[1]),
                        './font/orig_chars/cons/' + cons2[1] + '.svg',
                        'lr')
    else:
        fig = merge_two(cons_loc(cons[1]),
                        cons_loc(cons2[1]),
                        'tb')
    fig.save("./font/orig_chars/cons_cons/" + cons[1] + cons2[1] +".svg")

# cons + two_vows (seiaa too)
fig = merge_three(cons_loc('厶'),
                  vow_loc('丌'),
                  vow_loc('乍'), 'tbr')
fig.save("./font/orig_chars/cons_two_vows/厶丌乍.svg")
