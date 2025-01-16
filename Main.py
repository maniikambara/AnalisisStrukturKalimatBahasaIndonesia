import tkinter as tk
from tkinter import scrolledtext
from Parser import ParserEngine

class SPOKParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Parser Pola Kalimat Bahasa Indonesia")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        try:
            self.parser_engine = ParserEngine()
            self.parser_initialized = True
        except Exception as e:
            self.parser_initialized = False
            self.init_error = f"Kesalahan saat inisialisasi parser: {str(e)}"
        self.create_gui()

    def create_gui(self):
        self.create_header()
        self.create_team_frame()
        self.create_content()
        self.create_status_bar()
        if not self.parser_initialized:
            self.output_text.insert(tk.END, f"Error: {self.init_error}\n")
            self.status_bar.config(text="Parser gagal diinisialisasi", bg='red', fg='white')

    def create_header(self):
        header_frame = tk.Frame(self.root, bg='#2c3e50', pady=20)
        header_frame.pack(fill='x')
        title = tk.Label(header_frame, text="APLIKASI PARSER POLA KALIMAT BAHASA INDONESIA", font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white')
        title.pack()

    def create_team_frame(self):
        team_frame = tk.Frame(self.root, bg='#34495e', pady=15)
        team_frame.pack(fill='x')
        team_label = tk.Label(team_frame, text="Kelompok 2 Kelas E", font=('Arial', 12, 'bold'), bg='#34495e', fg='white')
        team_label.pack(anchor='w', padx=20)
        members = [
            "Aditya Premana Putra (2308561005)",
            "I Ketut Manik Ambarawan (2308561017)",
            "Angelica Audeska Sali (2308561047)",
            "I Made Yudi Pastika Putra (2308561095)",
            "I Putu Chandra Ananda Putra.S (2308561126)"
        ]
        for member in members:
            member_label = tk.Label(team_frame, text=member, font=('Arial', 10), bg='#34495e', fg='white')
            member_label.pack(anchor='w', padx=40)

    def create_content(self):
        content_frame = tk.Frame(self.root, pady=20, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True, padx=20)
        input_frame = tk.Frame(content_frame, bg='#f0f0f0')
        input_frame.pack(fill='x', pady=10)
        input_label = tk.Label(input_frame, text="Masukkan kalimat:", font=('Arial', 11), bg='#f0f0f0')
        input_label.grid(row=0, column=0, sticky='w')
        self.input_text = tk.Entry(input_frame, width=50, font=('Arial', 11))
        self.input_text.grid(row=0, column=1, padx=10, pady=5, sticky='we')
        analyze_button = tk.Button(input_frame, text="Analisis", command=self.analyze_sentence, bg='#3498db', fg='white', font=('Arial', 10, 'bold'), padx=10, pady=5)
        analyze_button.grid(row=0, column=2, padx=5, pady=5)
        input_frame.columnconfigure(1, weight=1)
        output_frame = tk.Frame(content_frame, bg='#f0f0f0')
        output_frame.pack(fill='both', expand=True)
        self.output_text = scrolledtext.ScrolledText(output_frame, width=70, height=20, font=('Arial', 10))
        self.output_text.pack(fill='both', expand=True, pady=10)

    def create_status_bar(self):
        self.status_bar = tk.Label(self.root, text="Siap untuk menganalisis kalimat", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg='#f0f0f0', font=('Arial', 10))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def analyze_sentence(self):
        self.output_text.delete(1.0, tk.END)
        sentence = self.input_text.get().strip()
        if not self.parser_initialized:
            self.output_text.insert(tk.END, "Error: Parser tidak tersedia!\n")
            self.status_bar.config(text="Parser gagal diinisialisasi", bg='red', fg='white')
            return
        if not sentence:
            self.output_text.insert(tk.END, "Error: Masukkan kalimat untuk dianalisis!\n")
            self.status_bar.config(text="Input kosong. Masukkan kalimat.", bg='red', fg='white')
            return
        try:
            self.status_bar.config(text="Menganalisis kalimat...", bg='#f0f0f0', fg='black')
            parse_result, message = self.parser_engine.analyze(sentence)
            if parse_result is None:
                self.output_text.insert(tk.END, f"Kalimat tidak valid!\n\nDetail: {message}\n")
                self.status_bar.config(text="Kalimat tidak valid", bg='red', fg='white')
                return
            self.output_text.insert(tk.END, "✓ Kalimat Valid!\n\n")
            self.output_text.insert(tk.END, "Struktur Kalimat:\n")
            self.output_text.insert(tk.END, "========================\n")
            self.display_structure(parse_result)
            self.output_text.insert(tk.END, "========================\n")
            self.status_bar.config(text="Analisis selesai", bg='green', fg='white')
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")
            self.status_bar.config(text="Terjadi kesalahan dalam analisis", bg='red', fg='white')

    def display_structure(self, structure):
        if isinstance(structure, dict):
            if 'Compound_Sentence' in structure:
                self.output_text.insert(tk.END, f"Kalimat Majemuk {structure.get('Compound_Sentence')}\n")
            else:
                self.output_text.insert(tk.END, f"Subjek\t\t: {structure.get('Subjek')}\n")
                self.output_text.insert(tk.END, f"Predikat\t\t: {structure.get('Predikat')}\n")
                if structure.get('Objek'):
                    self.output_text.insert(tk.END, f"Objek\t\t: {structure.get('Objek')}\n")
                if structure.get('Keterangan'):
                    self.output_text.insert(tk.END, f"Keterangan\t\t: {structure.get('Keterangan')}\n")
        else:
            self.output_text.insert(tk.END, "Struktur kalimat tidak dikenali.\n")

def main():
    root = tk.Tk()
    SPOKParserGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
