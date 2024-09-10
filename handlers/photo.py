from handlers import master as h_master

# Handled images
from PIL import Image

# System modules
from os import path 

import requests
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

def save_url(image_url:str) -> list:
    """Save Photo from URL \n
    
    Keyword arguments:\n
    image_url (str): URL from image
    Return: [bool, file_dir]
    """
    response = False
    file_dir = "Is not a Image (png, jpeg, jpg)" 

    if re.match(r".*\.(jpg|jpeg|png)$", image_url.lower()) is not None:
        try:
            # Download the photo using requests
            response = requests.get(image_url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Save the downloaded file
            file_location = path.join(direct, image_url.split('/')[-1])
            with open(file_location, "wb") as f:
                f.write(response.content)

            response = True
            file_dir = file_location

        except requests.RequestException as e:
            print(f">>> Error: {str(e)}")

    return [response, file_dir]

def process(file_path:str, ia:bool=False, deposit:bool=False) -> dict:
    """Process Image\n
    
    Keyword arguments:\n
    file_path: Image's directory\n
    ai (bool): False -> REGEX function True -> GPT recognise \n
    deposit (bool): False -> Invoice function True -> Deposit function \n

    # Invoice data
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
        }

    # Deposit data \n
    Return: { \n
        "title":"deposit_0.jpeg", \n
        "response":true, \n
        "process": { \n
            "amount":"$1000", \n
            "receipt_number": "2042016", \n
            "destination_account":"2670" \n
        }                                   \n                                
    } 
    """
    return h_master.make_decision(file_path, ia, deposit)

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