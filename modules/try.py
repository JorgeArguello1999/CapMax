import io
from google.cloud import vision
import pandas as pd

def detect_document(path):
    """Detects document features in an image."""
    client = vision.ImageAnnotatorClient.from_service_account_file('../.venv/credentials_vision_api.json')

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    documents = response.full_text_annotation.pages

    for page in documents:
        for block in page.blocks:
            print('\nBlock confidence:', block.confidence)

            for paragraph in block.paragraphs:
                print('Paragraph confidence:', paragraph.confidence)

                words = paragraph.words
                for word in words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print('Word text:', word_text)

# Replace with the path to your image
image_path = '../uploads/prueba.jpg'

detect_document(image_path)