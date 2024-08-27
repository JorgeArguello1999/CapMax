# Google SDK
from google.cloud import vision_v1p3beta1 as vision
from google.oauth2 import service_account

# Environment
from os import getenv
from dotenv import load_dotenv
load_dotenv()

# Credentials 
credentials_json = getenv('GOOGLE_CLOUD_CREDENTIALS')

# Detect text
def text_detect(file_path:str) -> str:
    """Google Text Detection (OCR)\n
    
    Keyword arguments:\n
    file_path: (str) Directory of photo \n
    Return: (str) All text from photo\n
    """
    
    # Google Cloud Client Vision
    credentials = service_account.Credentials.from_service_account_file(credentials_json)
    vision_client = vision.ImageAnnotatorClient(credentials=credentials)

    text_detected = "No Image"
    try:
        # Load image
        with open(file_path, "rb") as imagen:
            binary_image = imagen.read()
        content = binary_image

        # Detec image text content
        image = vision.Image(content=content)
        result = vision_client.document_text_detection(image=image)
        text_detected = result.full_text_annotation
        text_detected = text_detected.text

    except Exception as e:
        text_detected = str(e)

    return text_detected

if __name__ == "__main__":
    content = text_detect('../uploads/prueba_2.jpg')
    print(content)