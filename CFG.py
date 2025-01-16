from Database import get_word_categories

class CFG:
    def __init__(self):
        words = get_word_categories() or {}
        self.grammar = {
            "S": ["Kalimat_Sederhana", "Kalimat_Majemuk_Setara", "Kalimat_Majemuk_Bertingkat"],
            "Kalimat_Sederhana": ["SP", "SPO", "SPPel", "SPK", "SPOPel", "SPOK"],
            "SP": ["SUBJEK PREDIKAT"],
            "SPO": ["SUBJEK PREDIKAT OBJEK"],
            "SPPel": ["SUBJEK PREDIKAT PELengkap"],
            "SPK": ["SUBJEK PREDIKAT KETERANGAN"],
            "SPOPel": ["SUBJEK PREDIKAT OBJEK PELengkap"],
            "SPOK": ["SUBJEK PREDIKAT OBJEK KETERANGAN"],
            "Kalimat_Majemuk_Setara": [
                "SPK KONJ_SETARA SPK", "SPK KONJ_SETARA SP", "SPK KONJ_SETARA SPPel",
                "SPO KONJ_SETARA SP", "SPO KONJ_SETARA SPO", "SP KONJ_SETARA SPO"
            ],
            "Kalimat_Majemuk_Bertingkat": [
                "SP KONJ_BERTINGKAT SPPel",
                "SP KONJ_BERTINGKAT P",
                "SP KONJ_BERTINGKAT POK",
                "SPO KONJ_BERTINGKAT SPO",
                "SP KONJ_BERTINGKAT SPK",
                "SP KONJ_BERTINGKAT SP"
            ],
            "KETERANGAN": words.get('partikel', []) + words.get('adverbia', []),
            "KONJ_SETARA": words.get('konjungsi_koordinatif', []),
            "KONJ_BERTINGKAT": words.get('konjungsi_subordinatif', []),
            "PELapek": words.get('adjektiva', []) + words.get('adverbia', []) + words.get('kiasan', []),
            "POK": words.get('nomina', []) + words.get('pron', []) + words.get('adjektiva', []),
            "SUBJEK": words.get('nomina', []) + words.get('pron', []),
            "PREDIKAT": words.get('verba', []),
            "OBJEK": words.get('nomina', []) + words.get('pron', [])
        }

    def get_grammar(self):
        return self.grammar

    def validate_sentence_structure(self, words):
        grammar = self.grammar
        clauses = []
        current_clause = []
        current_konj = None

        for word in words:
            if word in grammar['KONJ_SETARA']:
                if current_clause:
                    clauses.append(current_clause)
                    current_clause = []
                current_konj = 'KONJ_SETARA'
                clauses.append([word, current_konj])
            elif word in grammar['KONJ_BERTINGKAT']:
                if current_clause:
                    clauses.append(current_clause)
                    current_clause = []
                current_konj = 'KONJ_BERTINGKAT'
                clauses.append([word, current_konj])
            else:
                current_clause.append(word)

        if current_clause:
            clauses.append(current_clause)

        if len(clauses) == 1:
            return self.validate_simple_sentence(clauses[0])
        else:
            print(clauses)
            compound_type = self.determine_compound_type(clauses)
            return {'Compound_Sentence': compound_type} if compound_type else None

    def determine_compound_type(self, clauses):
        setara_patterns = [
            ["SPK", "KONJ_SETARA", "SPK"], ["SPK", "KONJ_SETARA", "SP"],
            ["SPK", "KONJ_SETARA", "SPPel"], ["SPO", "KONJ_SETARA", "SP"],
            ["SPO", "KONJ_SETARA", "SPO"], ["SP", "KONJ_SETARA", "SPO"]
        ]
        bertingkat_patterns = [
            ["SP", "KONJ_BERTINGKAT", "SPPel"],
            ["SP", "KONJ_BERTINGKAT", "P"],
            ["SP", "KONJ_BERTINGKAT", "POK"],
            ["SPO", "KONJ_BERTINGKAT", "SPO"],
            ["SP", "KONJ_BERTINGKAT", "SPK"],
            ["SP", "KONJ_BERTINGKAT", "SP"]
        ]
        clause_types = []
        konj_type = None

        for clause in clauses:
            if isinstance(clause, list) and len(clause) <= 2 and clause[1] in ['KONJ_SETARA', 'KONJ_BERTINGKAT']:
                konj_type = clause[1]
                clause_types.append(konj_type)
            else:
                validation = self.validate_simple_sentence(clause)
                if validation:
                    if validation['Objek'] and validation['Keterangan']:
                        clause_types.append("SPOK")
                    elif validation['Objek']:
                        clause_types.append("SPO")
                    elif validation['Keterangan']:
                        clause_types.append("SPK")
                    else:
                        clause_types.append("SP")
                else:
                    clause_types.append(None)

        print(clause_types)
        if clause_types in setara_patterns:
            return "Setara"
        if clause_types in bertingkat_patterns:
            return "Bertingkat"
        return None

    def validate_simple_sentence(self, words):
        print (words)
        length = len(words)
        grammar = self.grammar
        if length == 2 and words[0] in grammar['SUBJEK'] and words[1] in grammar['PREDIKAT']:
            return {'Subjek': words[0], 'Predikat': words[1], 'Objek': None, 'Keterangan': None}
        if length == 3:
            if words[0] in grammar['SUBJEK'] and words[1] in grammar['PREDIKAT']:
                if words[2] in grammar['OBJEK']:
                    return {'Subjek': words[0], 'Predikat': words[1], 'Objek': words[2], 'Keterangan': None}
                if words[2] in grammar['PELapek'] or words[2] in grammar['KETERANGAN']:
                    return {'Subjek': words[0], 'Predikat': words[1], 'Objek': None, 'Keterangan': words[2]}
        if length == 4:
            if (words[0] in grammar['SUBJEK'] and words[1] in grammar['PREDIKAT'] and
                words[2] in grammar['OBJEK'] and (words[3] in grammar['PELapek'] or words[3] in grammar['KETERANGAN'])):
                return {'Subjek': words[0], 'Predikat': words[1], 'Objek': words[2], 'Keterangan': words[3]}
            if (words[0] in grammar['SUBJEK'] and words[1] in grammar['PREDIKAT'] and words[2], words[3] in grammar ['KETERANGAN']):
                return {'Subjek': words[0], 'Predikat': words[1], 'Objek': None, 'Keterangan': words[2] + ' ' + words[3]}

        if length == 5:
            if (words[0] in grammar['SUBJEK'] and words[1] in grammar['PREDIKAT'] and
                words[2] in grammar['OBJEK'] and (words[3], words[4] in grammar['PELapek'] or words[3], words[4] in grammar['KETERANGAN'])):
                return {'Subjek': words[0], 'Predikat': words[1], 'Objek': words[2], 'Keterangan': words[3] + ' ' + words[4]}
        return None
