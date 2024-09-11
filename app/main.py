# FastApi modules
from fastapi import HTTPException
from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile
from fastapi import Form

# HTML response
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Optional
from typing import Optional

# Modules
from handlers import photo

# Load env 
from dotenv import load_dotenv
from os import makedirs 
from os import getenv
from os import path
load_dotenv()

# DEV or PRO
_debug = getenv('DEBUG')
docs = None if _debug != 'True' else '/docs'
redoc = None if _debug != 'True' else '/redoc'

# 'uploads/' directory
dire = 'app/uploads/'
if not path.exists(dire): 
    try: 
        makedirs(dire)
        print(f'>>> Directory {dire} created...')
    except Exception as e:
        print(f'>>> Error: {str(e)}')

else: 
    print(f'>>> Directory {dire} exists')

# Start FastAPI
app = FastAPI(
    docs_url=docs,
    redoc_url=redoc,
)

# Templates dir
templates = Jinja2Templates(directory="app/templates")
# Static Files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Home
@app.get('/', response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
    
# Photo
@app.post("/photo/")
async def upload_photo(
    file: Optional[UploadFile] = File(None),
    ia: Optional[bool] = Form(False), 
    deposit: Optional[bool] = Form(False),
    image_url: Optional[str] = Form(None)
):

    if file and image_url:
        if file.filename: 
            raise HTTPException(status_code=400, detail="Cannot upload both file and URL at the same time.")

    try:
        if file and file.filename: # Check if file exist 
            response, file_location = photo.save(file=file)

        elif image_url:  # URL
            response, file_location = photo.save_url(image_url=image_url)

        else:
            raise HTTPException(status_code=400, detail="No valid image file or URL provided.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


    print(response)
    print(file_location)

    # Process photo
    print(f'>>> Image URL: {image_url}')
    print(f'>>> IA use: {ia}')
    print(f'>>> Deposit mode: {deposit}')

    try: 
        response = True
        process = photo.process(file_location, ia, deposit)
    except Exception as e: 
        response = False
        process = f"Problem with your data please try again with new data" 
        print(f'>>> Error: {str(e)}')

    # Delete photo
    delete = photo.delete(file_location)

    if response and delete:
        response = True

    return {
        "title": file.filename if file else path.basename(file_location),
        "response": response,
        "process": process
    }