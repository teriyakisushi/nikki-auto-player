from typing import Dict


class LangManager:
    def __init__(self, lang_code: str = 'cn'):
        self.lang_code = lang_code
        self.texts: Dict[str, str] = {}
        self.load_language()

    def load_language(self):
        try:
            if self.lang_code == 'en':
                from .en import TEXTS
            else:
                from .cn import TEXTS
            self.texts = TEXTS
        except ImportError:
            from .cn import TEXTS
            self.texts = TEXTS

    def get_text(self, key: str, default: str = '') -> str:
        return self.texts.get(key, default)


_lang_manager = LangManager()


def get_text(key: str, default: str = '') -> str:
    return _lang_manager.get_text(key, default)


t = get_text
