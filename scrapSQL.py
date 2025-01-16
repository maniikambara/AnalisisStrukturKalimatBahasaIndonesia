import mysql.connector
from mysql.connector import Error
import json

def scrape_kbbi_database(host, user, password, database, output_file):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        if connection.is_connected():
            print("Terhubung ke MySQL database")
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT word, arti FROM dictionary WHERE type = 2"
            cursor.execute(query)
            records = cursor.fetchall()
            
            categories = {
                'adjektiva': set(),
                'verba': set(),
                'nomina': set(),
                'kiasan': set(),
                'pron': set(),
                'arkais': set(),
                'adverbia': set(),
                'partikel': set()
            }
            
            kategori_kata = {
                'adjektiva': ['adjektiva'],
                'verba': ['verba'],
                'nomina': ['nomina'],
                'kiasan': ['kiasan'],
                'pron': ['pron'],
                'arkais': ['arkais'],
                'adverbia': ['adverbia'],
                'partikel': ['partikel']
            }
            
            for record in records:
                word = record['word'].strip().lower()
                arti = record['arti'].lower()
                
                for kategori, keywords in kategori_kata.items():
                    if any(kata in arti for kata in keywords):
                        categories[kategori].add(word)
            
            for kategori in categories:
                categories[kategori] = sorted(categories[kategori])
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(categories, f, indent=4, ensure_ascii=False)
            
            print(f"Data berhasil disimpan di {output_file}")

    except Error as e:
        print(f"Error: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Koneksi ke MySQL ditutup")

if __name__ == "__main__":
    host = 'localhost'
    user = 'root'
    password = 'root'
    database = 'kbbi'
    output_file = 'output.json'
    
    scrape_kbbi_database(host, user, password, database, output_file)
