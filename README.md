# jyutcitzi-code
The Python code used for generating the fonts and keyboards in [jyutcitzi-font](https://github.com/jyutcitzi/jyutcitzi-fonts) and [jyutcitzi-RIME](https://github.com/jyutcitzi/jyutcitzi-RIME) respectively.


## How to Reproduce the Jyutcitzi Fonts and Keyboards
```
# Reproduce Jyutcitzi Fonts
cd font
fontforge extract_glyphs_from_fonts.py
python make_chars_fonts.py
fontforge make_font_fonts.py

# Reproduce Jyutcitzi Keyboards
cd ..
python rime_chars.py > rime/jyutcitzi_web.dict.yaml
python rime_chars_font.py > rime/jyutcitzi_font.dict.yaml
python make_compound.py web > rime/jyutcitizi_web.compound.dict.yaml
python make_compound.py font > rime/jyutcitzi_font.compound.dict.yaml
python make_lettered.py core > rime/jyutcitzi_core.lettered.dict.yaml
python make_lettered.py web > rime/jyutcitzi_web.lettered.dict.yaml
python make_lettered.py font > rime/jyutcitzi_font.lettered.dict.yaml
python make_jyutcit_phrases.py web > jyutcitzi_web.jyutcit_phrases.dict.yaml
python make_jyutcit_phrases.py font > jyutcitzi_font.jyutcit_phrases.dict.yaml
```
Note: make_jyutcit_phrases relies on ./rime/custom_list.txt

## Requirements
svgutils, FontForge
