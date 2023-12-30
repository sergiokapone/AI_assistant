import os
import tempfile
import PyPDF2
import re

from typing import Union, List


# read only digital PDF book which more 1000 sings
def extract_text_from_pdf(pdf_sources: List[Union[str, bytes, tempfile.SpooledTemporaryFile]]):
    for pdf_source in pdf_sources:
        reader = PyPDF2.PdfReader(pdf_source)
        _pdf_text = ""

        for page in reader.pages:
            _pdf_text += page.extract_text()

        print(type(_pdf_text))

        # Очищаем текст от недопустимых символов и тегов
        cleaned_text = re.sub(r'[\d/.]', '', _pdf_text)

        # Записываем полученный текст в текстовый файл
        output_file = 'output.txt'
        mode = 'a' if os.path.exists(output_file) else 'w'
        with open(output_file, mode, encoding='utf-8') as file:
            file.write(cleaned_text)

        print(f"Text from PDF file '{pdf_source}' has been written to 'output.txt'")


if __name__ == "__main__":

    # Спрашиваем у пользователя, сколько файлов он хотел бы загрузить
    num_files = int(input("How many PDF files would you like to upload? - "))

    pdf_paths = []
    # Просим пользователя ввести путь к каждому файлу
    for i in range(num_files):
        while True:
            pdf_path = input(f"Please enter full path to PDF #{i + 1}: ")
            # Проверяем, является ли указанный путь файлом PDF
            if not pdf_path.lower().endswith(".pdf"):
                print("!!! Specified file is not a PDF file.")
                continue
            # Проверяем, существует ли указанный файл
            if not os.path.isfile(pdf_path):
                print("!!! The specified file does not exist.")
                continue
            break
        pdf_paths.append(pdf_path)

    # Вызываем функцию extract_text_from_pdf с указанными путями к PDF-файлам
    extract_text_from_pdf(pdf_paths)

