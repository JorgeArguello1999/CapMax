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

# Requests
import requests

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

    if file:
        # Save the uploaded file
        response, file_location = photo.save(file)
    elif image_url:
        try:
            # Download the photo using requests
            response = requests.get(image_url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Save the downloaded file
            file_location = path.join(dire, image_url.split('/')[-1])
            with open(file_location, "wb") as f:
                f.write(response.content)
            response = True
        
        except requests.RequestException as e:
            print(f">>> Error: {str(e)}")
            raise HTTPException(status_code=400, detail='Failed to download image')
    
    if not file_location:
        raise HTTPException(status_code=400, detail='No image file or URL provided')

    # Process photo
    print(f'>>> IA use: {ia}')
    print(f'>>> Deposit mode: {deposit}')
    process = photo.process(file_location, ia, deposit)

    # Delete photo
    delete = photo.delete(file_location)

    if response and delete:
        response = True

    return {
        "title": file.filename if file else path.basename(file_location),
        "response": response,
        "process": process
    }