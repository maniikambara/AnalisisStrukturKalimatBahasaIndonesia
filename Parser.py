import ply.lex as lex
from Database import get_word_categories
from CFG import CFG
import re

word_categories = get_word_categories()

tokens = [
    'ADJEKTIVA', 'VERBA', 'NOMINA', 'KATA_KIASAN',
    'PRONOMINA', 'KATA_PERCAPAKAN', 'ARKAIS', 'ADVERBIA',
    'KONJ_SETARA', 'KONJ_BERTINGKAT', 'PARTIKEL'
]

def create_regex(category):
    words = word_categories.get(category, [])
    if not words:
        return r'a^'
    sorted_words = sorted(words, key=lambda x: len(x.split()), reverse=True)
    return r'\b(?:' + '|'.join(map(re.escape, sorted_words)) + r')\b'

t_ADJEKTIVA = create_regex('adjektiva')
t_VERBA = create_regex('verba')
t_NOMINA = create_regex('nomina')
t_KATA_KIASAN = create_regex('kiasan')
t_PRONOMINA = create_regex('pron')
t_ARKAIS = create_regex('arkais')
t_ADVERBIA = create_regex('adverbia')
t_PARTIKEL = create_regex('partikel')
t_KONJ_SETARA = create_regex('konjungsi_koordinatif')
t_KONJ_BERTINGKAT = create_regex('konjungsi_subordinatif')

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Karakter tidak dikenali: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

class ParserEngine:
    def __init__(self):
        self.cfg = CFG()

    def tokenize_sentence(self, sentence):
        lexer.input(sentence.lower())
        return [(tok.type, tok.value) for tok in iter(lexer.token, None)]

    def analyze(self, sentence):
        tokens = self.tokenize_sentence(sentence)
        if not tokens:
            return (None, "Tidak ada kata yang dikenali dalam kalimat.")

        actual_words = [word for _, word in tokens]
        spok_structure = self.cfg.validate_sentence_structure(actual_words)
        return (spok_structure, "Kalimat Valid!") if spok_structure else (None, "Kalimat tidak valid atau tidak sesuai struktur")

    def get_spok_structure(self, token_info):
        return token_info
