import json
import os

class SPOKDatabase:
    def __init__(self, data_file='output.json'):
        self.data = {
            'adjektiva': [],
            'verba': [],
            'nomina': [],
            'kiasan': [],
            'pron': [],
            'arkais': [],
            'adverbia': [],
            'partikel': [],
            'konjungsi_koordinatif': self.initialize_konjungsi_koordinatif(),
            'konjungsi_subordinatif': self.initialize_konjungsi_subordinatif()
        }
        self.load_data(data_file)

    def initialize_konjungsi_koordinatif(self):
        konjungsi_koordinatif = [
            "dan", "atau", "tetapi", "melainkan", "namun", "sekalipun",
            "justru", "tapi", "bahkan", "lalu", "kemudian", "jadi"
        ]
        return konjungsi_koordinatif

    def initialize_konjungsi_subordinatif(self):
        konjungsi_subordinatif = [
            "karena", "sebab", "supaya", "agar", "sehingga",
            "ketika", "bila", "apabila", "jika", "walaupun",
            "meskipun", "biar", "padahal", "guna",
            "oleh karena itu", "karena itu", "sehingga"
        ]
        return konjungsi_subordinatif

    def load_data(self, data_file):
        if not os.path.exists(data_file):
            print(f"File {data_file} tidak ditemukan.")
            return
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data_dict = json.load(f)
            
            for kategori in self.data.keys():
                if kategori in ['konjungsi_koordinatif', 'konjungsi_subordinatif']:
                    continue
                if kategori in data_dict:
                    self.data[kategori] = data_dict[kategori]
                else:
                    print(f"Kategori '{kategori}' tidak ditemukan dalam {data_file}.")
        
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

    def get_word_categories(self):
        return self.data

def get_word_categories():
    db = SPOKDatabase()
    return db.get_word_categories()
