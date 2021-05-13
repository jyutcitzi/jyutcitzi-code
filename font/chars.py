import itertools
import os.path
# enable_jcz_font = True
auto_dot_add = True
dot_char = "·" if auto_dot_add else ""


乃旡_hex = 0xe1ae
厶介_hex = 0xe27e
gghz_font_chars = [('唔','𠄡','𠄡'),
                # ('嘅','旡','旡'), # bug:
                # bug: 好嘅,傻嘅,值得嘅 can be both 旡 and 丩旡 depending on context
                # set as 丩旡 for now
                ('國','囻','囻'),
                ('咁','恁','恁'),
                ('嘢','野','野'),
                ('咗','徂','徂'),
                ('唑','徂','徂'),
                ('哋','倛','倛'),
                ('嚟','黎','蒞'), # this hack should work for now
                # ('嚟',('黎','蒞'),('黎','蒞')),
                ('呢','尼',chr(乃旡_hex)), # hack to get more options
                ('而','爾','爾'),
                ('依','邇','邇'),
                ('緊','亙','亙'),
                ('𡁵','亙','亙'),
                ('啫','嗟','嗟'),
                ('嗮','曬',chr(厶介_hex)),
                ('晒','曬',chr(厶介_hex)),
                ('曬','曬',chr(厶介_hex)),
                ('嗰','亇',chr(0xe6a6)), # todo: add the other two options
                ('啲','少々',chr(0xe6a7)),
                # ('咪','五係',chr(0xe6a8))
                # disabled since only used in hai mai and mai
                ('噉','工耳',chr(0xe6a9)),
                ('喺','彳糸',chr(0xe6aa)),
                ('啱','正岩',chr(0xe6ab)),
                ('自由','自由',chr(0xe6ac))
                ]

def get_hex_dict(file_loc, ng_tilde=False):
    # Note: "tilde" is supposed to mean tick here
    hex_dict = {'々': '々'}
    with open(file_loc) as file:
        for line in file.read().splitlines():
            hex_str, chars = line.split(" ")
            chars = chars.replace("oe","居")
            hex_dict[chars] = chr(int(hex_str, 16))
    if ng_tilde:
        hex_dict['五`'] = hex_dict['ng`']
        hex_dict['五.'] = hex_dict['m`']
    else:
        hex_dict['五`'] = hex_dict['ng_m']
        hex_dict['五.'] = hex_dict['ng_m']

    for _ , web_form, font_form in gghz_font_chars:
        hex_dict[web_form] = font_form
    hex_dict['五係'] = chr(0xe6a8)
    hex_dict['忄禾子'] = chr(0xe6ad)
    hex_dict['忄厶云'] = chr(0xe6ae)
    hex_dict['黹禾子'] = chr(0xe6af)
    hex_dict['黹厶云'] = chr(0xe6b0)
    hex_dict['黹兒'] = chr(0xe6b1)
    hex_dict['黹臣'] = chr(0xe6b2)
    hex_dict['乍`戈'] = chr(0xe6b3)
    hex_dict['天尺戈'] = chr(0xe6b4)
    hex_dict['口勺`'] = chr(0xe6b5)
    hex_dict['忄夫么'] = chr(0xe6b6)
    hex_dict['扌爻丂'] = chr(0xe6b7)
    hex_dict['辶厶円'] = chr(0xe6b8)
    hex_dict['正_flip'] = chr(0xe6b9)
    return hex_dict

# remove "char.py" and append "fonts/mapping.txt" to get exact file location
hex_dict = get_hex_dict(__file__[:-8] + "fonts/mapping.txt", ng_tilde=False)

# todo: replace phrases dictionary with goigaakhonzi
# todo: 五好, 五可

# todo: divide phrases between 丩旡· and 旡  (嘅)
# should only contain uncontested characters
goigaakhonzi = gghz_font_chars + \
                [('唉','介`',hex_dict['介`']), # +'〡'
                 ('哎','介`',hex_dict['介`']), # +'〡'
                 ('噃','比个',hex_dict['比个']), # +'〣'
                 ('啩','古乍',hex_dict['古乍']), # +"〣"
                 ('吔','央乍',hex_dict['央乍']), # +'〡'
                 ('嘞','力百',hex_dict['力百']), # +'〣'
                 ('囖','力个',hex_dict['力个']), # +'〡'
                 ('嗱','乃乍',hex_dict['乃乍']), # +'〤'
                 ('阿','乍`',hex_dict['乍`']) # +'〣'
                 # 啝， 禾个〥·
                ]

# contested usually in terms of pitch, but also actual romanization
contested_chars = ['吖','呀','啊','㗎','嘅','吓','啦','喇','哩','囉','咯',
                   '喎','咋','啫','哈','哦','𠳏']

gghz_guess = [('吖','乍`',hex_dict['乍`']),
              ('呀','乍`',hex_dict['乍`']),
              ('啊','乍`',hex_dict['乍`']),
              ('㗎','丩乍',hex_dict['丩乍']),
              ('嘅','丩旡',hex_dict['丩旡']),
              ('吓','亾乍',hex_dict['亾乍']),
              ('啦','力乍',hex_dict['力乍']),
              ('喇','力乍',hex_dict['力乍']),
              ('哩','力旡',hex_dict['力旡']),
              ('囉','力个',hex_dict['力个']),
              ('咯','力个',hex_dict['力个']), # error: could be lok3
              ('喎','禾个',hex_dict['禾个']),
              ('咋','止乍',hex_dict['止乍']),
              ('啫','止旡',hex_dict['止旡']), # error: could be zek1
              ('哈','亾乍',hex_dict['亾乍']),
              ('哦','个`',hex_dict['个`']),
              ('𠳏','此旡',hex_dict['此旡'])
              ]

ngs = [("ng","五`"),
       ("m","五."),
       ("ng",chr(0x20121)),
       ("m",chr(0x20121)),
       ("ng",chr(0x20121) + "`"),
       ("m",chr(0x20121) + ".")]
special_cons = [("ng",chr(0x20121)), ("m",chr(0x20121))]

#比并文夫大天乃力止此厶央丩臼亾爻古夸禾乍介丂彡万生甲压百兮久今云亙十乜仄旡丌了壬円正夾叐尺子么欠千丁頁必夕个丐冇干王匃乇乎会本工末玉居丈勺句卂𥘅仒元乙𠄡亇々
consonants = [('b','比','⿱'), # uni6bd4
              ('p','并','⿰'), # uni5e76
              ('m','文','⿱'), # uni6587
              ('f','夫','⿰'), # uni529b
              ('d','大','⿱'),
              ('t','天','⿱'),
              ('n','乃','⿰'),
              ('l','力','⿰'),
              ('z','止','⿰'),
              ('c','此','⿱'),
              ('s','厶','⿱'),
              ('j','央','⿱'),
              ('g','丩','⿰'),
              ('k','臼','⿱'),
              ('h','亾','⿰'),
              ('ng','爻','⿱'),
              ('gw','古','⿰'),
              ('kw','夸','⿰'),
              ('w','禾','⿱')]
r_only = [('r','ㄖ','⿰')]
ext_cons = r_only + [('v','圭','⿰')]
e_en = [('e','亇'), ('en','艮')]
ext_vows = [('z','止')] + e_en
zcs = [('z','止','⿰'),
        ('c','此','⿱'),
        ('s','厶','⿱')]
zcsh = [('zh','止亾'),
        ('ch','此亾'),
        ('sh','厶亾')]
mnpt = [('m','文','⿱'),
        ('n','乃','⿰'),
        ('p','并','⿰'),
        ('t','天','⿱')]

# deprecated
# two_cons = []
two_cons = [('st','厶天'), # [OBSOLETE?] start
            ('sg','厶丩'), # scour (sgour)
            ('sk','厶臼'), # scare (skaair)
            ('sb','厶比'), # spear
            ('sj','厶央'), # sjang, sheer (sjier)
            ('sw','厶禾'), # sweat, sweet
            ('sl','厶力'), # slow
            ('sn','厶乃'), # snare
            ('cw','此禾'), # train (cwain)
            ('pj','并央'), # pjoi
            ]

two_cons_aug = [('sp','厶并'), # sparrow
             ('sm','厶文'), # smear
             ('sf','厶夫'), # sphere
             ('sd','厶大'), # start
             ('mw','文禾'), # Mandarin mo #('sh','厶亾'), # [DUPLICATE] shower
             ('bl','比力'), # black
             ('pl','并力'), # plore
             ('fl','夫力'), # floor
             # ('zl','止力'),
             ('cl','此力'), # clock
             ('gl','丩力'), # glock
             ('kl','臼力'), # clock (klok)
             ('sz','厶止'), # szwak coe (structure)
             ('lw','力禾'), # Mandarin lo, ('sc','厶此'), # [OBSOLETE] scared
             # ('zs','止厶'), #
             # ('cs','此厶'),
             ('bj','比央'), # bjarn (bjiaawn)
             ('mj','文央'), # mjoi
             ('fj','夫央'), # fière (fjiew)
             ('dj','大央'), # jeff (djef)
             ('tj','天央'), # beetje (beitje)
             ('zj','止央'), # zjaa6 bong6
             ('cj','此央'), # cji
             ('gj','丩央'), # jeer (gjier)
             ('kj','臼央'), # kyaa! (kjaa)
             # ('gwj','古央'),
             # ('kwj','夸央'),
             # ('wj','禾央'),

             ('sh','厶亾'),  # share
             # ('sng','厶爻'),
             ('sgw','厶古'), # squeal (sgwil)
             ('skw','厶夸'), # scribe (skraaib)
             ('bw','比禾'), # Mandarin 波, bread
             ('pw','并禾'), # Mandarin 破, prance
             ('fw','夫禾'), # Mandarin 佛, friend, fret
             ('dw','大禾'), # Mandarin 多, dread
             ('tw','天禾'), # Mandarin 托, treat
             ('nw','乃禾'),
             ('zw','止禾'), # Mandarin 做, dread (zwead)
             # ('jw','央禾'),
             ('hw','亾禾'), # Mandarin 火 (fire) hwhere?
             ('rw','ㄖ禾'), # Mandarin若; was ('ts','天厶') in font v1 # [OBSOLETE]
             ('ngw','爻禾')
             ]
three_cons = [('sbw','厶比禾'), # spread (sbread)
                ('spw','厶并禾'), # spread
                ('smw','厶文禾'), # smreka
                # ('sfw','厶夫禾'), #
                ('sdw','厶大禾'), # sdwakcoe
                ('stw','厶天禾'), # stretch, stream
                # ('snw','厶乃禾'),
                # ('slw','厶力禾'),
                ('szw','厶止禾'), # stream
                ('scw','厶此禾'), # [OBSOLETE] e.g. stream
                ('sjw','厶央禾'), # e.g. shread
                ('shw','厶亾禾'), # Mandarin 說, e.g. shread
                # ('sngw','厶爻禾')
                ]


## third iteration, caters for Standard Mandarin and Hakka varieties
two_cons_aug2 = [('hj','亾央'),
                 ('nj','乃央'),
                 ('lj','力央'),
                 ('ngj','爻央'),
                 ('zh','止亾'),
                 ('ch','此亾'),
                 ('wl','禾力')] # a Cantonese representation of English 'r'
three_cons_2 = [('zhw','止亾禾'),
                 ('chw','此亾禾')]

cons_yuen = [('l','力','⿰'),
            ('z','止','⿰'),
            ('c','此','⿱'),
            ('s','厶','⿱'),
            ('j','央','⿱')]

cons_yue = cons_yuen + [('n','乃','⿰')]

two_cons_aug_toneless = [('sp','厶并'), # sparrow
                         ('sm','厶文'), # smear
                         ('sf','厶夫'), # sphere
                         ('sd','厶大'), # start
                         ('bl','比力'), # black
                         ('pl','并力'), # plore
                         ('fl','夫力'), # floor
                         ('cl','此力'), # clock
                         ('gl','丩力'), # glock
                         ('kl','臼力'), # clock (klok)
                         ('sz','厶止'), # szwak coe (structure)
                         ('sgw','厶古'), # squeal (sgwil)
                         ('skw','厶夸'), # scribe (skraaib)
                         ]

two_cons_aug_toneful = [
             ('mw','文禾'), # ('sh','厶亾'), # [DUPLICATE] shower
             ('lw','力禾'), # ('sc','厶此'), # [OBSOLETE] scared
             ('bj','比央'), # bjarn (bjiaawn)
             ('mj','文央'), # mjoi
             ('fj','夫央'), # fière (fjiew)
             ('dj','大央'), # jeff (djef)
             ('tj','天央'), # beetje (beitje)
             ('zj','止央'), # zjaa6 bong6
             ('cj','此央'), # cji
             ('gj','丩央'), # jeer (gjier)
             ('kj','臼央'), # kyaa! (kjaa)
             # ('gwj','古央'),
             # ('kwj','夸央'),
             # ('wj','禾央'),
             ('sh','厶亾'),  # share
             # ('sng','厶爻'),
             ('bw','比禾'), # Mandarin 波, bread
             ('pw','并禾'), # Mandarin 破, prance
             ('fw','夫禾'), # Mandarin 佛, friend, fret
             ('dw','大禾'), # Mandarin 多, dread
             ('tw','天禾'), # Mandarin 托, treat
             ('nw','乃禾'),
             ('zw','止禾'), # Mandarin 做, dread (zwead)
             # ('jw','央禾'),
             ('hw','亾禾'), # Mandarin 火 (fire) hwhere?
             ('rw','ㄖ禾'), # Mandarin若; was ('ts','天厶') in font v1 # [OBSOLETE]
             ('ngw','爻禾')
             ]

three_cons_toneless = [('sbw','厶比禾'), # spread (sbread)
                        ('spw','厶并禾'), # spread
                        ('smw','厶文禾'), # smreka
                        # ('sfw','厶夫禾'), #
                        ('sdw','厶大禾'), # sdwakcoe
                        ('stw','厶天禾'), # stretch, stream
                        # ('snw','厶乃禾'),
                        # ('slw','厶力禾'),
                        ('szw','厶止禾'), # stream
                        ('scw','厶此禾'), # [OBSOLETE] e.g. stream
                        ('sjw','厶央禾'), # e.g. shread
                        # ('sngw','厶爻禾')
                        ]
three_cons_toneful = [('shw','厶亾禾')]
many_cons_opt_pitch = two_cons + two_cons_aug_toneful + two_cons_aug2 \
                      + three_cons_2 + three_cons_toneful
many_cons_no_pitch = two_cons_aug_toneless + three_cons + three_cons_toneless
many_cons = many_cons_opt_pitch + many_cons_no_pitch
## end third iteration


end_cons = [('b','比','⿱'), # uni6bd4
              ('f','夫','⿰'), # uni529b
              ('d','大','⿱'),
              ('l','力','⿰'),
              ('z','止','⿰'),
              ('c','此','⿱'),
              ('j','央','⿱'),
              ('g','丩','⿰'),
              # ('k','臼','⿱'),
              ('w','禾','⿱')]

multi_end_cons = [('sp','厶并'), # wasp
                ('sm','厶文'), # spasm
                ('st','厶天'), # cast, gunst
                ('sk','厶臼'), # cask
                ('zj','止央'), # french
                ('cj','此央'), # witch
                ('sj','厶央'), # flesh
                ('zh','止亾'), # witch
                ('ch','此亾'), # witch
                ('sh','厶亾'), # cash
                ('bl','比力'), # pebble = bou
                ('pl','并力'), # apple = pou
                ('fl','夫力'), # felafel = fou
                ('sl','厶力'), # weasl = sou
                ('zl','止力'), # weasel = zou
                ('wl','禾力'), # bowl = nothing

                # ft? eg. soft (sof)
                # gl? google
                ]

vowels = [('aa','乍'),
          ('aai','介'),
          ('aau','丂'),
          ('aam','彡'), # old version: 三
          ('aan','万'),
          ('aang','生'),
          ('aap','甲'),
          ('aat','压'), # 甴
          ('aak','百'),
          ('ai','兮'),
          ('au','久'),
          ('am','今'),
          ('an','云'),
          ('ang','亙'),
          ('ap','十'),
          ('at','乜'),
          ('ak','仄'),
          ('e','旡'),
          ('ei','丌'),
          ('eu','了'),
          ('em','壬'),
          ('en','円'),
          ('eng','正'),
          ('ep','夾'),
          ('et','叐'), # old version: 犮
          ('ek','尺'),
          ('i','子'),
          ('iu','么'),
          ('im','欠'),
          ('in','千'),
          ('ing','丁'),
          ('ip','頁'),
          ('it','必'),
          ('ik','夕'),
          ('o','个'),
          ('oi','丐'),
          ('ou','冇'),
          ('on','干'),
          ('ong','王'),
          ('ot','匃'),
          ('ok','乇'),
          ('u','乎'),
          ('ui','会'),
          ('un','本'),
          ('ung','工'),
          ('ut','末'),
          ('uk','玉'),
          ('oe','居'),
          ('oeng','丈'),
          ('oek','勺'),
          ('eoi','句'),
          ('eon','卂'),
          ('eot','𥘅'),
          ('yu','仒'),
          ('yun','元'),
          ('yut','乙')]


vow_sups = [('om','个','文'),
            ('um','乎','文'),
            ('oem','居','文'),
            ('yum','仒','文'),
            ('yung','仒','爻'),
            ('op','个','并'),
            ('up','乎','并'),
            ('oep','居','并'),
            ('yup','仒','并'),
            ('yuk','仒','臼')]

vow_vows = [
          ('aai','介'),
          ('aau','丂'),
          ('ai','兮'),
          ('au','久'),
          ('ei','丌'),
          ('eu','了'),
          ('iu','么'),
          ('oi','丐'),
          ('ou','冇'),
          ('ui','会'),
          ('eoi','句')]

pure_vowels = [('aa','乍'),
              ('e','旡'),
              ('i','子'),
              ('o','个'),
              ('u','乎'),
              ('oe','居'),
              ('yu','仒')]

# numbers (optional to use them)
## OLD SYSTEM
# pitches_only = [('1','〡'),
#                 ('2','〢'),
#                 ('3','〣'),
#                 ('4','〤'),
#                 ('5','〥'),
#                 ('6','〦')]
## NEW SYSTEM
pitches_only = [('1','¯'),
                 ('2','´'),
                 ('3','`'),
                 ('4','⁼'),
                 ('5','˝'),
                 ('6','ﾞ'),
                 ('7','\''), # alternative to 1
                 ('8',"\"")] # alternative to 4

separators = [('.','·'),('..','。'),
              (',','，'),
              ('~','～'),
              ('/','、'),
              ('<','《'),
              ('>','》'),
              ('[','「'),
              ('[','【'),
              (']','」'),
              (']','】'),]
compositions = [('lr','⿰'),
                ('tb','⿱'),
                ('enc','⿺')]

# special designated Chinese characters
special_chars = [('go2','彳固'), ('go2','个'), ('go2','亇'), ('go2','ケ'),
                 ('di1','少々'),
                 ('ge3','旡'),
                 ('me1','羋'),('me1','咩'),
                 ('mai2','袂'),
                 ('mai3','五係'),
                 ('gam3','恁'),
                 ('gam2','工耳'),
                 ('hai2','彳糸'),
                 ('je5','野'),
                 ('dei6','倛'),
                 ('lei4','黎'),('lei4','蒞'),
                 ('ngaam1','正岩'),
                 ('ji1','依'),
                 ('ne1','尼'),
                 ('gan2','亙'),
                 ('ji4','爾'),('ji4','邇'),
                 ('ze1','姐'),('ze1','嗟'),
                 ('zek1','啫'),
                 ('zo2','徂'),
                 ('saai3','曬'),('saai3','厶介')]

# note: the following logograms cannot be rendered currently
# 1. ping3 (represents the opposite of zing3)
# 2. the simplified version of '義'
particles = [
('zi2','黹'),
('jyun4','玄'),
('din6','申'),('din6','电'),
('zing3','正'),('zeng3','正'),
('ping3','叵'),('po2','叵'),
('ji6','義'),
('zik6','直'),
('tin1','天'),('tin1','兲'),
('got1','㕦'),
('god1','㕦')
]

# some common chinese radicals
particles += [
('cou2','艹'),
('seoi2','氵'),
('muk6','木'),
('hau2','口'),
('sam1','忄'),
('jin4','訁'),
('kiusi1','糹'),
('kiu5si1','糹'),
('si6','礻'),
('ji1','⻂'),
('sau2','扌'),
('gwo1','戈'),
('zau2','⻎'),
]

particles += [(pair[0][:-1], pair[1]) for pair in particles] + [('zj','自由')]

# provides:
# 1. jyutping w/o pitch
# 2. jyutping with pitch
# 3a. english word
# 3. original loanword w/o pitch
examples = [('hoeng1gong2','香港'),('hoenggong','香港'),
            ('skip1tong4','厶臼頁·堂'),('skiptong','厶臼頁·堂'),
            ('aa3sjang1','阿·厶央生'),('aasjang','阿·厶央生'),
            ('pjoihau2seoi2','并央丐·口水'),('pjoihauseoi','并央丐·口水'),
            ('desi','大旡·厶子'),('des','大旡·厶`'),
            ('saa1a3','厶乍乍'),('saaa','厶乍乍'),

            ('wisan','忄禾子·忄厶云'),('wisan','黹禾子·黹厶云'),('wisan','黹兒·黹臣'),
            ('wi1san4','忄禾子·忄厶云'),('wi1san4','黹禾子·黹厶云'),('wi1san4','黹兒·黹臣'),
            ('reason','忄禾子·忄厶云'),('reason','黹禾子·黹厶云'),('reason','黹兒·黹臣'),

            ('aatek','乍`戈·天尺戈'),('aa3tek1','乍`戈·天尺戈'),('attack','乍`戈·天尺戈'),

            ('oek3hei3','口勺`·亾丌'),# ('oekhei','口勺`·亾丌'),
            ('urkhei3','口勺`·亾丌'),('urkhei','口勺`·亾丌'),
            ('fiu','忄夫么'),('fiu1','忄夫么'),('feel','忄夫么'),
            ('ngaau','扌爻丂'),('ngaau1','扌爻丂'),
            ('fans','夫円．厶子'),
            ('sen','辶厶円'),('sen1','辶厶円'),('send','辶厶円'),
            ('bytheway','比介．大乍．禾丌')
            ]
# examples = [(ins, outs + dot_char) for ins, outs in examples]

spec_uni_particles = [(['go','go2'],'彳固'), # 0x55f0
                    (['di','di1'],'少々'), # 0x5572
                    (['mai','mai3'],'ng係'),
                    (['gam','gam2'],'工耳'), # 0x5649
                    (['hai','hai2'],'彳糸'), # 0x55ba
                    (['ngaam','ngaam1'],'正岩'),
                    (['zj'],'自由')]
spec_uni_phrases = [(None,'忄禾子'),
                    (None,'忄厶云'),
                    (None,'黹禾子'),
                    (None,'黹厶云'),
                    (None,'黹兒'),
                    (None,'黹臣'),
                    (None,'乍`戈'),
                    (None,'天尺戈'),
                    (None,'口勺`')]
spec_uni_phrases_2 = [(['fiu','fiu1','feel'],'忄夫么'),
                      (['ngaau','ngaau1'],'扌爻丂'),
                      (['sen','sen1','send'],'辶厶円')]
