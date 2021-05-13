import itertools

scz_jh = [('zj','止央'), # french
        ('cj','此央'), # witch
        ('sj','厶央'), # flesh
        ('zh','止亾'), # witch
        ('ch','此亾'), # witch
        ('sh','厶亾'), # shower
        ]

# m
m_vowel = [('aam','彡'), # old version: 三
            ('am','今'),
            ('em','壬'),
            ('im','欠')]
m_vow_sup = [('om','个文'),
             ('um','乎文'),
             ('oem','居文'),
             ('yum','仒文')]
m_cons = [('p','并','⿰'), # uni5e76
          ('f','夫','⿰'), # uni529b
          ('d','大','⿱'),
          ('t','天','⿱'),
          ('k','臼','⿱')]
m_multi_cons = [('sp','厶并'), # spear
                ('st','厶天'), # start
                ('sk','厶臼'), # scare
                ('bl','比力'), # black
                ('pl','并力'), # plore
                ('ml','文力'), # plore
                ('sl','厶力'), # plore
                ] + scz_jh

# n
n_vowel = [('aan','万'),
          ('an','云'),
          ('en','円'),
          ('in','千'),
          ('on','干'),
          ('un','本'),
          ('eon','卂'),
          ('yun','元')]
n_cons = [('d','大','⿱'),
          ('t','天','⿱'),
          ('z','止','⿰'),
          ('c','此','⿱'),
          ('k','臼','⿱')]
n_multi_cons = [('sp','厶并'), # spear
                ('st','厶天'), # gunst
                ('sk','厶臼'), # minsk
                ] + scz_jh

# ng
ng_vowel = [('aang','生'),
           ('ang','亙'),
           ('eng','正'),
           ('ing','丁'),
           ('ong','王'),
           ('ung','工')]
ng_vow_sup = [('oeng','居爻'),
              ('yung','仒爻')]
ng_cons = [('d','大','⿱'),
          ('t','天','⿱'),
          ('z','止','⿰'),
          ('c','此','⿱'),
          ('k','臼','⿱')]
ng_multi_cons = [('sp','厶并'), # spear
                ('st','厶天'), # start
                ('sk','厶臼'), # scare
                ('gl','丩力')] + scz_jh # plore


# p
p_vowel = [('aap','甲'),
          ('ap','十'),
          ('ep','夾'),
          ('ip','頁')]
p_vow_sup = [('op','个并'),
            ('up','乎并'),
            ('oep','居并'),
            ('yup','仒并')]
p_cons = [('d','大','⿱'),
          ('t','天','⿱')
          ]
p_multi_cons = [('st','厶天'), # start
                ('sk','厶臼'), # scare
                ('pl','并力')] + scz_jh # plore


# t
t_vowel = [('aat','压'), # 甴
           ('at','乜'),
           ('et','叐'), # old version: 犮
           ('it','必'),
           ('ot','匃'),
           ('ut','末'),
           ('eot','𥘅'),
           ('yut','乙')]
t_cons = [('t','天','⿱'),
          ('z','止','⿰'),
          ('c','此','⿱')]
t_multi_cons = [('tl','天力')] + scz_jh

# k
k_vowel = [('aak','百'),
           ('ak','仄'),
           ('ek','尺'),
           ('ik','夕'),
           ('ok','乇'),
           ('uk','玉'),
           ('oek','勺')]
k_vow_sup = [('yuk','仒臼')]
k_cons = [('t','天','⿱'),
          ('z','止','⿰'),
          ('c','此','⿱')]
k_multi_cons = [('kl','臼力')] + scz_jh

# get combinations
m_v_c_iterator = itertools.product(m_vowel, m_cons)
m_v_cc_iterator = itertools.product(m_vowel, m_multi_cons)
m_vs_c_iterator = itertools.product(m_vow_sup, m_cons)
m_vs_cc_iterator = itertools.product(m_vow_sup, m_multi_cons)

n_v_c_iterator = itertools.product(n_vowel, n_cons)
n_v_cc_iterator = itertools.product(n_vowel, n_multi_cons)
# n_vs_c_iterator = itertools.product(n_vow_sup, n_cons)
# n_vs_cc_iterator = itertools.product(n_vow_sup, n_multi_cons)

ng_v_c_iterator = itertools.product(ng_vowel, ng_cons)
ng_v_cc_iterator = itertools.product(ng_vowel, ng_multi_cons)
ng_vs_c_iterator = itertools.product(ng_vow_sup, ng_cons)
ng_vs_cc_iterator = itertools.product(ng_vow_sup, ng_multi_cons)

p_v_c_iterator = itertools.product(p_vowel, p_cons)
p_v_cc_iterator = itertools.product(p_vowel, p_multi_cons)
p_vs_c_iterator = itertools.product(p_vow_sup, p_cons)
p_vs_cc_iterator = itertools.product(p_vow_sup, p_multi_cons)

t_v_c_iterator = itertools.product(t_vowel, t_cons)
t_v_cc_iterator = itertools.product(t_vowel, t_multi_cons)
# t_vs_c_iterator = itertools.product(t_vow_sup, t_cons)
# t_vs_cc_iterator = itertools.product(t_vow_sup, t_multi_cons)

k_v_c_iterator = itertools.product(k_vowel, k_cons)
k_v_cc_iterator = itertools.product(k_vowel, k_multi_cons)
k_vs_c_iterator = itertools.product(k_vow_sup, k_cons)
k_vs_cc_iterator = itertools.product(k_vow_sup, k_multi_cons)

vEnd_c_iterator = itertools.chain(
    m_v_c_iterator, n_v_c_iterator, ng_v_c_iterator, p_v_c_iterator, t_v_c_iterator, k_v_c_iterator
)

vEnd_cc_iterator = itertools.chain(
    m_v_cc_iterator, n_v_cc_iterator, ng_v_cc_iterator, p_v_cc_iterator, t_v_cc_iterator, k_v_cc_iterator
)

vs_c_iterator = itertools.chain(
    m_vs_c_iterator, ng_vs_c_iterator, p_vs_c_iterator, k_vs_c_iterator
) # n_vs_c_iterator, t_vs_c_iterator

vs_cc_iterator = itertools.chain(
    m_vs_cc_iterator, ng_vs_cc_iterator, p_vs_cc_iterator, k_vs_cc_iterator
) # n_vs_cc_iterator, t_vs_cc_iterator
