from handlers import master as h_master

from PIL import Image

import shutil
import uuid
import re
import os

# Directory 
direct = "app/uploads/"

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

def process(file_path:str, ia:bool=False) -> dict:
    """Process Image\n
    
    Keyword arguments:\n
    file_path: Image's directory\n
    ai (bool): False -> REGEX function True -> GPT recognise \n
    Return: { \n
        'rucs' : {
            'vendor': int,
            'client': int
        },\n
        'dates' : str 'DD/MM/YYYY',\n
        'total_value' : int,\n
        'factura_auth' : str\n
        'factura_n' : str\n
        'ai': bool
        } \n
    """
    return h_master.make_decision(file_path, ia)

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