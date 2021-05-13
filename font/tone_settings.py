import itertools
import svgutils
import sys
import os

def glyph_fromfile(file):
    fig = svgutils.transform.fromfile(file)
    if fig.height is not None and fig.width is not None:
        pass
    elif fig.height is None and fig.width is None:
        fig.height, fig.width = 1010, 1000
    else:
        raise NotImplementedError
    return fig
consts = {
    "./fonts/PMingLiU/Regular/": {
        "¯":{"shrink_factor": 0.8, "x_fac":0.75, "y_fac": 0.08, "y_offset": 0},
        "´":{"shrink_factor": 0.8, "x_fac":0.75, "y_fac": 0.1, "y_offset": 0.05},
        "`":{"shrink_factor": 0.8, "x_fac":0.75, "y_fac": 0.11, "y_offset": -0.05},
        "\'":{"shrink_factor": 0.8, "x_fac":0.82, "y_fac": 0.11, "y_offset": -0.05},
        "\"":{"shrink_factor": 0.8, "x_fac":0.75, "y_fac": 0.11, "y_offset": -0.05}
    },
    "./fonts/SourceHanSansHC/ExtraLight/": {
        "¯":{"shrink_factor": 0.7, "x_fac":0.66, "y_fac": 0.08, "y_offset": -0.05},
        "´":{"shrink_factor": 0.8, "x_fac":0.60, "y_fac": 0.13, "y_offset": 0.03},
        "`":{"shrink_factor": 0.8, "x_fac":0.67, "y_fac": 0.13, "y_offset": 0.03},
        "\'":{"shrink_factor": 0.8, "x_fac":0.78, "y_fac": 0.13, "y_offset": -0.05},
        "\"":{"shrink_factor": 0.8, "x_fac":0.72, "y_fac": 0.13, "y_offset": -0.05}
    },
    "./fonts/SourceHanSansHC/Light/": {
        "¯":{"shrink_factor": 0.7, "x_fac":0.66, "y_fac": 0.08, "y_offset": -0.05},
        "´":{"shrink_factor": 0.8, "x_fac":0.60, "y_fac": 0.13, "y_offset": 0.03},
        "`":{"shrink_factor": 0.8, "x_fac":0.67, "y_fac": 0.13, "y_offset": 0.03},
        "\'":{"shrink_factor": 0.8, "x_fac":0.78, "y_fac": 0.13, "y_offset": -0.05},
        "\"":{"shrink_factor": 0.8, "x_fac":0.72, "y_fac": 0.13, "y_offset": -0.05}
    },
    "./fonts/SourceHanSansHC/Regular/": {
        "¯":{"shrink_factor": 0.7, "x_fac":0.66, "y_fac": 0.08, "y_offset": -0.05},
        "´":{"shrink_factor": 0.8, "x_fac":0.60, "y_fac": 0.13, "y_offset": 0.03},
        "`":{"shrink_factor": 0.8, "x_fac":0.67, "y_fac": 0.13, "y_offset": 0.03},
        "\'":{"shrink_factor": 0.7, "x_fac":0.78, "y_fac": 0.13, "y_offset": -0.05},
        "\"":{"shrink_factor": 0.7, "x_fac":0.71, "y_fac": 0.13, "y_offset": -0.05}
    },
    "./fonts/SourceHanSansHC/Normal/": {
        "¯":{"shrink_factor": 0.7, "x_fac":0.66, "y_fac": 0.08, "y_offset": -0.05},
        "´":{"shrink_factor": 0.8, "x_fac":0.60, "y_fac": 0.13, "y_offset": 0.03},
        "`":{"shrink_factor": 0.8, "x_fac":0.67, "y_fac": 0.13, "y_offset": 0.03},
        "\'":{"shrink_factor": 0.7, "x_fac":0.78, "y_fac": 0.13, "y_offset": -0.05},
        "\"":{"shrink_factor": 0.7, "x_fac":0.71, "y_fac": 0.13, "y_offset": -0.05}
    },
    "./fonts/SourceHanSansHC/Medium/": {
        "¯":{"shrink_factor": 0.7, "x_fac":0.66, "y_fac": 0.08, "y_offset": -0.05},
        "´":{"shrink_factor": 0.8, "x_fac":0.60, "y_fac": 0.13, "y_offset": 0.03},
        "`":{"shrink_factor": 0.8, "x_fac":0.67, "y_fac": 0.13, "y_offset": 0.03},
        "\'":{"shrink_factor": 0.65, "x_fac":0.78, "y_fac": 0.13, "y_offset": -0.05},
        "\"":{"shrink_factor": 0.65, "x_fac":0.71, "y_fac": 0.13, "y_offset": -0.05}
    },
    "./fonts/SourceHanSansHC/Heavy/": {
        "¯":{"shrink_factor": 0.65, "x_fac":0.67, "y_fac": 0.10, "y_offset": -0.03},
        "´":{"shrink_factor": 0.65, "x_fac":0.62, "y_fac": 0.15, "y_offset": 0.06},
        "`":{"shrink_factor": 0.65, "x_fac":0.72, "y_fac": 0.15, "y_offset": 0.06},
        "\'":{"shrink_factor": 0.50, "x_fac":0.79, "y_fac": 0.13, "y_offset": 0},
        "\"":{"shrink_factor": 0.50, "x_fac":0.72, "y_fac": 0.13, "y_offset": 0}
    },
    "./fonts/SourceHanSansHC/Bold/": {
        "¯":{"shrink_factor": 0.65, "x_fac":0.67, "y_fac": 0.10, "y_offset": -0.03},
        "´":{"shrink_factor": 0.65, "x_fac":0.62, "y_fac": 0.15, "y_offset": 0.06},
        "`":{"shrink_factor": 0.65, "x_fac":0.72, "y_fac": 0.15, "y_offset": 0.06},
        "\'":{"shrink_factor": 0.55, "x_fac":0.75, "y_fac": 0.13, "y_offset": 0},
        "\"":{"shrink_factor": 0.55, "x_fac":0.67, "y_fac": 0.13, "y_offset": 0},
        "\'":{"shrink_factor": 0.50, "x_fac":0.79, "y_fac": 0.13, "y_offset": 0},
        "\"":{"shrink_factor": 0.50, "x_fac":0.72, "y_fac": 0.13, "y_offset": 0}
    },
    "./fonts/SourceHanSerifTC/ExtraLight/": {
        "¯":{"shrink_factor": 0.7, "x_fac":0.72, "y_fac": 0.08, "y_offset": -0.05},
        "´":{"shrink_factor": 0.8, "x_fac":0.67, "y_fac": 0.13, "y_offset": 0},
        "`":{"shrink_factor": 0.8, "x_fac":0.73, "y_fac": 0.13, "y_offset": 0},
        "\'":{"shrink_factor": 0.8, "x_fac":0.79, "y_fac": 0.13, "y_offset": -0.05},
        "\"":{"shrink_factor": 0.8, "x_fac":0.74, "y_fac": 0.13, "y_offset": -0.05}
    },
    "./fonts/SourceHanSerifTC/Light/": {
        "¯":{"shrink_factor": 0.7, "x_fac":0.72, "y_fac": 0.08, "y_offset": -0.05},
        "´":{"shrink_factor": 0.8, "x_fac":0.67, "y_fac": 0.13, "y_offset": 0},
        "`":{"shrink_factor": 0.8, "x_fac":0.73, "y_fac": 0.13, "y_offset": 0},
        "\'":{"shrink_factor": 0.8, "x_fac":0.75, "y_fac": 0.13, "y_offset": -0.05},
        "\"":{"shrink_factor": 0.8, "x_fac":0.67, "y_fac": 0.13, "y_offset": -0.05},
        "\'":{"shrink_factor": 0.8, "x_fac":0.79, "y_fac": 0.13, "y_offset": -0.05},
        "\"":{"shrink_factor": 0.8, "x_fac":0.74, "y_fac": 0.13, "y_offset": -0.05}
    },
    "./fonts/SourceHanSerifTC/Regular/": {
        "¯":{"shrink_factor": 0.7, "x_fac":0.72, "y_fac": 0.08, "y_offset": -0.05},
        "´":{"shrink_factor": 0.8, "x_fac":0.67, "y_fac": 0.13, "y_offset": 0},
        "`":{"shrink_factor": 0.8, "x_fac":0.73, "y_fac": 0.13, "y_offset": 0},
        "\'":{"shrink_factor": 0.8, "x_fac":0.79, "y_fac": 0.13, "y_offset": -0.05},
        "\"":{"shrink_factor": 0.8, "x_fac":0.74, "y_fac": 0.13, "y_offset": -0.05}
    },
    "./fonts/SourceHanSerifTC/Medium/": {
        "¯":{"shrink_factor": 0.7, "x_fac":0.72, "y_fac": 0.08, "y_offset": -0.05},
        "´":{"shrink_factor": 0.8, "x_fac":0.67, "y_fac": 0.13, "y_offset": 0},
        "`":{"shrink_factor": 0.8, "x_fac":0.73, "y_fac": 0.13, "y_offset": 0},
        "\'":{"shrink_factor": 0.7, "x_fac":0.79, "y_fac": 0.13, "y_offset": -0.05},
        "\"":{"shrink_factor": 0.7, "x_fac":0.74, "y_fac": 0.13, "y_offset": -0.05}
    },
    "./fonts/SourceHanSerifTC/SemiBold/": {
        "¯":{"shrink_factor": 0.7, "x_fac":0.72, "y_fac": 0.08, "y_offset": -0.05},
        "´":{"shrink_factor": 0.8, "x_fac":0.67, "y_fac": 0.13, "y_offset": 0},
        "`":{"shrink_factor": 0.8, "x_fac":0.73, "y_fac": 0.13, "y_offset": 0},
        "\'":{"shrink_factor": 0.60, "x_fac":0.79, "y_fac": 0.13, "y_offset": 0},
        "\"":{"shrink_factor": 0.60, "x_fac":0.74, "y_fac": 0.13, "y_offset": 0}
    },
    "./fonts/SourceHanSerifTC/Bold/": {
        "¯":{"shrink_factor": 0.7, "x_fac":0.72, "y_fac": 0.08, "y_offset": -0.05},
        "´":{"shrink_factor": 0.8, "x_fac":0.67, "y_fac": 0.13, "y_offset": 0},
        "`":{"shrink_factor": 0.8, "x_fac":0.73, "y_fac": 0.13, "y_offset": 0},
        "\'":{"shrink_factor": 0.60, "x_fac":0.79, "y_fac": 0.13, "y_offset": 0},
        "\"":{"shrink_factor": 0.60, "x_fac":0.74, "y_fac": 0.13, "y_offset": 0}
    },
    "./fonts/SourceHanSerifTC/Heavy/": {
        "¯":{"shrink_factor": 0.7, "x_fac":0.72, "y_fac": 0.08, "y_offset": -0.05},
        "´":{"shrink_factor": 0.8, "x_fac":0.67, "y_fac": 0.13, "y_offset": 0.02},
        "`":{"shrink_factor": 0.8, "x_fac":0.73, "y_fac": 0.13, "y_offset": 0.02},
        "\'":{"shrink_factor": 0.60, "x_fac":0.79, "y_fac": 0.13, "y_offset": 0},
        "\"":{"shrink_factor": 0.60, "x_fac":0.74, "y_fac": 0.13, "y_offset": 0}
    },
    "./fonts/SourceHanSansHWHC/Regular/": {
        "¯":{"shrink_factor": 0.7, "x_fac":0.66, "y_fac": 0.08, "y_offset": -0.05},
        "´":{"shrink_factor": 0.8, "x_fac":0.60, "y_fac": 0.13, "y_offset": 0.02},
        "`":{"shrink_factor": 0.8, "x_fac":0.70, "y_fac": 0.15, "y_offset": 0.03},
        "\'":{"shrink_factor": 0.60, "x_fac":0.71, "y_fac": 0.13, "y_offset": 0},
        "\"":{"shrink_factor": 0.60, "x_fac":0.71, "y_fac": 0.13, "y_offset": 0}
    },
    "./fonts/SourceHanSansHWHC/Bold/": {
        "¯":{"shrink_factor": 0.7, "x_fac":0.66, "y_fac": 0.08, "y_offset": -0.05},
        "´":{"shrink_factor": 0.7, "x_fac":0.60, "y_fac": 0.13, "y_offset": 0.05},
        "`":{"shrink_factor": 0.7, "x_fac":0.70, "y_fac": 0.13, "y_offset": 0.05},
        "\'":{"shrink_factor": 0.60, "x_fac":0.74, "y_fac": 0.13, "y_offset": 0},
        "\"":{"shrink_factor": 0.60, "x_fac":0.74, "y_fac": 0.13, "y_offset": 0}
    },
}

diacritics = "¯´`"
def add_tone(jcz_file, font_folder, num):
    if num == 7:
        double_tone = False
        tone_char = "'"
    elif num == 8:
        double_tone = False
        tone_char = '"'
    else:
        double_tone = num >= 4
        tone_char = diacritics[(num - 1) % 3]
    tone_file = font_folder + "/chars/"+tone_char+".svg"
    orig_jcz = glyph_fromfile(jcz_file)
    tone = glyph_fromfile(tone_file)

    # get constants
    shrink_factor = consts[font_folder][tone_char]["shrink_factor"]
    move_x_factor = consts[font_folder][tone_char]["x_fac"]
    move_y_factor = consts[font_folder][tone_char]["y_fac"]
    y_offset = consts[font_folder][tone_char]["y_offset"]
    fig = svgutils.transform.SVGFigure(orig_jcz.width, orig_jcz.height)
    if double_tone:
        tone2 = glyph_fromfile(tone_file)
        plot3 = tone2.getroot()
        plot3.scale_xy(int(orig_jcz.width)/int(tone.width)*shrink_factor,int(orig_jcz.height)/int(tone.height)*shrink_factor)
        plot3.moveto(int(orig_jcz.width)*move_x_factor, int(orig_jcz.width)*(y_offset+move_y_factor)) # 150, 20

    plot1, plot2 = orig_jcz.getroot(), tone.getroot()

    plot2.scale_xy(int(orig_jcz.width)/int(tone.width)*shrink_factor,int(orig_jcz.height)/int(tone.height)*shrink_factor)
    plot2.moveto(int(orig_jcz.width)*move_x_factor,int(orig_jcz.width)*y_offset) # 150, 0
    #130/int(fig.width)
    plot1.scale_xy(0.8,1)
    fig.append([plot1, plot2] + ([plot3] if double_tone else []))
    return fig
