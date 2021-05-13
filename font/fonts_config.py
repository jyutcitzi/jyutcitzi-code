fonts = {'PMingLiU': {
                'folder': './fonts/PMingLiU/',
                'weights': ['Regular'],
                'generateChar': False,
                'referenceFont': 'PMingLiU'
         },
        'SourceHanSerifTC': {
            'folder': './fonts/SourceHanSerifTC/',
            'weights': ['SemiBold','ExtraLight','Heavy','Light','Medium','Regular','Bold'],
            'generateChar': True,
            'referenceFont': 'SourceHanSerifTW'
         },
        'SourceHanSansHC': {
            'folder': './fonts/SourceHanSansHC/',
            'weights': ['Bold','ExtraLight','Heavy','Light','Medium','Normal','Regular'],
            'generateChar': True,
            'referenceFont': 'SourceHanSansHK'
         },
         'SourceHanSansHWHC': {
            'folder': './fonts/SourceHanSansHWHC/',
            'weights': ['Bold','Regular'],
            'generateChar': True,
            'referenceFont': None
         }
        }

fontdirs = []
for fontname in fonts:
    dirname = fonts[fontname]['folder']
    for weight in fonts[fontname]['weights']:
        fontdirs.append(dirname + weight + '/')
