import pandas as pd
from pdf2docx import Converter
import docx
import pandas as pd
from pdf2docx import Converter
import docx
import os

def pdf_to_docx(pdf_file, docx_file, encoding='utf-8'):
    """
    Convert a PDF file to a DOCX file using the specified encoding.

    Args:
        pdf_file (str): The path to the PDF file to be converted.
        docx_file (str): The path to save the converted DOCX file.
        encoding (str, optional): The encoding to be used for the conversion. Defaults to 'utf-8'.
    """
    cv = Converter(pdf_file)
    cv.convert(docx_file, encoding=encoding)
    cv.close()
    print(f"PDF file '{pdf_file}' converted to DOCX file '{docx_file}'")

def clean(text):
    """
    Cleans the given text by replacing specific characters with their corresponding replacements.

    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text.
    """
    replacements = {
        '֊': 'ŋ',
        'ջ': 'ɓ',
        'ս': 'ɗ',
        'ђ': 'ə',
        'ॣ': 'Ɓ',
        'փ': 'ĩ',
        '\u0b5a' : 'Ə',
        'ઞ' : 'Ŋ',
        '॥': 'ɗ',
        'qqn': "quelqu'un",
    }
    cleaned_text = text
    for char, replacement in replacements.items():
        cleaned_text = cleaned_text.replace(char, replacement)
    return cleaned_text

def main():
    pdf_path = '../docs/mdng-dictionary.pdf'
    docx_path = '../docs/mdng-dictionary.docx'
    
    pdf_to_docx(pdf_path, docx_path)
    
    doc = docx.Document(docx_path)
    texts = []
    sentence = ''
    
    for paragraph in doc.paragraphs[69:]:
        for run in paragraph.runs:
            if not run.bold and not run.italic:
                sentence += run.text
            if run.italic:
                text = [sentence, run.text]
                texts.append(text)
                sentence = ''
    
    for i in range(len(texts)):
        mdng_cleaned = clean(texts[i][0])
        fr_cleaned = clean(texts[i][1])
        texts[i] = texts[i] + ['. '.join(mdng_cleaned.split('.')[1:]), '. '.join(fr_cleaned.split('.')[2:])]
        texts[i][0] = '. '.join(mdng_cleaned.split('.')[:1])
        texts[i][1] = ''.join(fr_cleaned.split('.')[:2])
    
    df = pd.DataFrame(texts, columns=['mdng', 'fr', 'mdng-remain', 'fr-remain'])
    df.to_csv('../data/dictionary.csv', index=False)
    
    docsx_path = '../docs/mdng-dictionary.docx'
    if os.path.exists(docsx_path):
        os.remove(docsx_path)
        print(f"File '{docsx_path}' has been deleted.")
    else:
        print(f"File '{docsx_path}' does not exist.")

if __name__ == "__main__":
    main()
