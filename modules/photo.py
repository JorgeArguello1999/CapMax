from modules import google_vision as gv

from PIL import Image

import shutil
import uuid
import re
import os

# Directory 
direct = "uploads/"

# Suspends num of pixels
Image.MAX_IMAGE_PIXELS = None

def save(file) -> list:
    """Save Photo\n
    
    Keyword arguments:\n
    file: All data file\n
    Return: [bool, file_dir]
    """
    response = False
    try: 
        # Is image? 
        if re.match(r".*\.(jpg|jpeg|png)$", file.filename.lower()) is not None:
            file_location = f"{direct + str(uuid.uuid4()) + file.filename}"
            with open(file_location, "wb") as f:
                shutil.copyfileobj(file.file, f)
            response = True

        else: 
            file_location = "Is not a image (png, jpeg, jpg)"
    
    except Exception as e: 
        file_location = e

    return [response, file_location]

def process(file_path) -> str:
    """Process Image\n
    
    Keyword arguments:\n
    file_path: Image's directory\n
    Return: string from image\n
    """
    # Detect text
    text_detect = gv.text_detect(file_path=file_path)

    # Classify and search
    # text_detect = stda.Data(text_detect)
    # text_detect = text_detect.to_dict()

    return text_detect

def delete(file_path:str) -> bool:
    """Delete Photo\n
    
    Keyword arguments: \n
    file_path: Dir photo\n
    Return: bool
    """
    response = False
    try:
        os.remove(file_path)
        print("Successfull")
        response = True

    except FileNotFoundError:
        print(f"File doesn't exist: '{file_path}'")

    except PermissionError:
        print(f"Delete is not allowed: '{file_path}'.")

    except Exception as e:
        print(f"Error: {e}")

    return response