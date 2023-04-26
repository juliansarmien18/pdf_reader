from itertools import accumulate
import PyPDF2
import pdfplumber
from tabulate import tabulate

class PdfReader:
    def __init__(self, filename):
        self.file_name = filename
        self.pdf_file = open(filename, 'rb')
        self.pdf_reader = PyPDF2.PdfReader(self.pdf_file)
        self.num_pages = len(self.pdf_reader.pages)

    def read_all(self):
        for page_num in range(self.num_pages):
            page = self.pdf_reader.pages[page_num]
            print(f'pagina {page_num} : {page.extract_text()}')

    def search_text(self, search_text):
        for page_num in range(self.num_pages):
            page = self.pdf_reader.pages[page_num]
            text = page.extract_text()
            if search_text in text:
                print(f'La cadena de texto "{search_text}" se encontró en la página {page_num+1}')
                
    def extract_tables(self, page_number=None):
        column_widths = [12,11,32,25,23,37,14]
        with pdfplumber.open(self.file_name) as pdf:
            if page_number is None:
                pages = pdf.pages
            else:
                pages = [pdf.pages[page_number - 1]]
            for page in pages:
                table_settings = {
                    "horizontal_strategy": "lines",
                    "vertical_strategy": "text", 
                    "explicit_horizontal_lines": [0] + list(accumulate(column_widths))
                }
                header_settings = {
                    "horizontal_strategy": "lines",
                    "vertical_strategy": "lines", 
                }
                
                extracted_table = page.extract_table(table_settings)
                headers = page.extract_table(header_settings)[0]
                rows = extracted_table[1:]
        
                # crear una lista de diccionarios que contienen los datos de la tabla
                table = [dict(zip(headers, row)) for row in rows]
                #table = []
            return table

    def close(self):
        self.pdf_file.close()