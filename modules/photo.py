# Shutil for files
import shutil

# Unique code
import uuid

# Regular expresion
import re

# System 
import os

# Directory 
direct = "uploads/"

def save(file) -> list:
    """Save Photo
    
    Keyword arguments:
    file: All data file
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


def delete(file_path:str) -> bool:
    """Delete Photo
    
    Keyword arguments:
    file_path: Dir photo
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