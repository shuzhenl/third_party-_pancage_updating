

LOCALES = (
    # Language      Android iOS
    ('English',     'en',   'en'),
    ('Turkish',     'tr',   'tr'),
    ('Spanish',     'es',   'es'),
    ('German',      'de',   'de'),
    ('French',      'fr',   'fr'),
    ('Arabic',      'ar',   'ar'),
    ('Japanese',    'ja',   'ja'),
    ('Korean',      'ko',   'ko'),
    ('Danish',      'da',   'da'),
    ('Italian',     'it',   'it'),
    ('Dutch',       'nl',   'nl'),
    ('Portuguese',  'pt',   'pt'),
    ('Swedish',     'sv',   'sv'),
    ('Hebrew',      'iw',   'he'),
    ('Russian',     'ru',   'ru'),
    ('Polish',      'pl',   'pl'),
    ('Chinese (Traditional)', 'zh-rCN', 'zh-Hant'),
    ('Chinese (Simplified)', 'zh-rTW', 'zh-Hans')
)


class Locale(object):

    def __init__(self,language, android_code, ios_code):
        self.language = language
        self.ios_code = ios_code
        self.android_code = android_code

    @classmethod
    def get_locale(cls, name):
        config = next(item for item in LOCALES if name == item[0])
        return Locale(*config)

    @classmethod
    def get_locale_from_ios_code(cls, ios_code):
        config = next(item for item in LOCALES if ios_code == item[2])
        return Locale(*config)
