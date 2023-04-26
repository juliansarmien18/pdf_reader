from pdf_reader import PdfReader

if __name__ == '__main__':
    prueba = PdfReader('prueba.pdf')
    tables = prueba.extract_tables(1)
    
    print(tables)