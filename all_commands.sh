cd lang_input
cd font

# generate the fonts
python extract_glyphs_from_fonts.py
python make_chars_fonts.py
fontforge make_font_fonts.py
cd .. # (out of font folder)

# generate the RIME keyboard
python rime_chars.py > rime/jyutcitzi_web.dict.yaml
python rime_chars_font.py > rime/jyutcitzi_font.dict.yaml
python make_compound.py web > rime/jyutcitizi_web.compound.dict.yaml
python make_compound.py font > rime/jyutcitzi_font.compound.dict.yaml
python make_lettered.py core > rime/jyutcitzi_core.lettered.dict.yaml
python make_lettered.py web > rime/jyutcitzi_web.lettered.dict.yaml
python make_lettered.py font > rime/jyutcitzi_font.lettered.dict.yaml
python make_jyutcit_phrases.py web > jyutcitzi_web.jyutcit_phrases.dict.yaml
python make_jyutcit_phrases.py font > jyutcitzi_font.jyutcit_phrases.dict.yaml
