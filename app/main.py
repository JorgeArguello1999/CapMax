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
    file_location = None
    response = False

    # Restrict not both at the same time
    if file.filename and image_url: 
        raise HTTPException(status_code=400, detail="Only one method URL or File no both at the same time")
    # Save the uploaded file
    if file and not image_url: response, file_location = photo.save(file=file)
    # Download image from url 
    if image_url: response, file_location = photo.save_url(image_url=image_url)
    # Any other file 
    if not response or file_location == None:
        raise HTTPException(status_code=400, detail='No valid image file or URL provided (jpg, jpeg, png)')

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