#!/usr/local/bin/fontforge
import fontforge
from chars import consonants, vowels, ext_cons, ext_vows, e_en
import chars
from fonts_config import fonts
# 喂，我哋唔係啱啱已經喺嗰度好咧啡噉噏咗你嗰啲咁𠵇𠺫嘅嘢㗎喇咩？戇鬮仔𣚕傾
#比并文夫大天乃力止此厶央丩臼亾爻古夸禾乍介丂彡万生甲压百兮久今云亙十乜仄旡丌了壬円正夾叐尺子么欠千丁頁必夕个丐冇干王匃乇乎会本工末玉居丈勺句卂𥘅仒元乙𠄡亇々㐅
#Apple LiGothic, Apple LiSung: 厶丩亾丂彡压円叐个匃会卂𥘅仒𠄡亇々
#Apple SD Gothic Neo, AppleGothic, AppleMyungjo, GungSeo: 并厶丩亾夸丂彡压亙乜旡丌叐么个丐冇匃乇会卂𥘅仒𠄡亇々
#Airal Unicode MS, Hannotate SC, HanziPen SC, Hiragino Sans GB, Lantinghei SC, LingWai SC, PingFang SC/TC, STFangsong, Wawati SC, Xingkai SC/TC: 𥘅𠄡
#Baoli SC/TC, SongTi SC/TC, Kaiti SC/TC, Libian SC/TC, LingWai TC, PingFang HK, STKaiti, STSong, NotoSansHK: 𠄡
#BiauKai: 厶丩亾丂彡压円叐个匃会卂𥘅仒𠄡亇々
#GB18030 Bitmap, STHeiti: 𥘅𠄡々
#Hannotate TC, HanziPen TC:丩丂𥘅仒𠄡
#Hei: 丩亾丂亙旡円夾叐頁冇匃卂𥘅仒𠄡亇
#Hiragino Maru Gothic ProN, Hiragino Mincho ProN: 亾压乜叐冇𥘅仒𠄡亇
#Hiragino Sans: 丩亾丂压乜丌叐么冇匃乇卂𥘅仒𠄡亇
#Hiragino Sans CNS: 丩亾丂压匃𥘅仒𠄡
#Kai: 丩亾丂亙旡円夾叐頁冇匃卂𥘅仒𠄡亇
#Klee: 丩亾丂压乜丌叐冇匃乇卂𥘅仒𠄡亇
#Lantinghei TC:丩亾丂压匃𥘅仒𠄡
#LiHei Pro: 𥘅仒𠄡
#LiSong Pro: 丩丂𥘅仒𠄡
#Nanum Gothic: 并厶丩亾夸丂彡压亙乜旡丌叐么个丐冇匃乇会卂𥘅仒𠄡亇々
#Osaka: 丩亾丂压乜丌叐么冇匃乇卂𥘅仒𠄡亇
#PCMyungjo: 并厶丩亾夸丂彡压亙乜旡丌叐么个丐冇匃乇会卂𥘅仒𠄡亇々
#Toppan Bunkyu Gothic/Mincho: 亾压叐冇𥘅仒𠄡亇
#Toppan Bunkyu Midashi Gothic/Mincho: 丩亾丂压乜丌叐么冇匃乇卂𥘅仒𠄡亇
#Tsukushi A Round Gothic: 丩亾丂压乜丌叐么冇匃乇卂𥘅仒𠄡亇
#Wawati TC:厶丩亾丂彡压円叐个匃会卂𥘅仒𠄡亇々
extra_chars = ['ㄨ','乂','𭕄','少','々','彳','固','係','耳','糸','正','岩','自','由','忄','黹','兒','臣','戈','口','扌','辶','区','五']
tone_chars = ['¯','´','`','\'','"']
for fontname in fonts:
    if not fonts[fontname]['generateChar']:
        # skip PMingLiu since the font itself doesn't contain all the components required for generating the JCZs
        # the original components were obtained from glyphwiki
        continue
    print('start '+fontname)
    dirname = fonts[fontname]['folder']
    for weight in fonts[fontname]['weights']:
        font = fontforge.open(dirname + weight + '/' + fontname + '-' + weight + '.ttf')
        font.em = 1000
        chars = tone_chars + [char[1] for char in consonants + vowels + ext_cons + e_en] + extra_chars# ( if fonts[fontname]['generateChar'] else tone_chars)
        for char in chars:
            if fontname == 'SourceHanSerifTC' and char == '𥘅':
                # use 朮 instead of 𥘅
                char = '朮'
            glyph = font.createChar(ord(char))
            glyph.export(dirname + weight +'/chars/'+ char + '.svg', pixelsize=200)

# need to create ng, 正_flip and 爻_tb

# use 居 instead of oe

# note:
# 1. no 𥘅 for PMingLiu, PingFang, BiauKai
# 2. no 厶,丩,亾,丂, 彡, 压, 円, 叐, 个, 匃, 会, 卂, 仒 for BiauKai
