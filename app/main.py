# FastApi modules
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
    print(f'>>> Directory {dire} exist')

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
async def upload_photo(file: UploadFile = File(...), ia:Optional[bool]=Form(False), deposit:Optional[bool]=Form(False)):
    # Save the file 
    response, file_location = photo.save(file)

    # Process photo
    print(f'>>> IA use: {ia}')
    print(f'>>> Deposit mode: {deposit}')
    process = photo.process(file_location, ia)

    # Delete photo
    delete = photo.delete(file_location)

    if response and delete: response = True
    else: False

    return {
        "title": file.filename,
        "response" :response,
        "process": process
    }