#! /usr/bin/env python
import fontforge

fonts = ["JyutcitziWithSourceHanSansHCHeavy",
         "JyutcitziWithSourceHanSansHCLight",
         "JyutcitziWithSourceHanSansHCMedium",
         "JyutcitziWithSourceHanSansHCRegular",
         "JyutcitziWithSourceHanSansHCNormal",
         "JyutcitziWithSourceHanSansHCBold",
         "JyutcitziWithSourceHanSansHCExtraLight"]
fonts = [fontforge.open(font) for font in fonts]
fonts[0].generateTtc ("JyutcitziWithSourceHanSansHC.ttc", fonts[1:]) , ttcflags = ("merge",)
