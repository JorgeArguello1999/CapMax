# FastApi modules
from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile

# HTML response
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

# Modules
from modules import photo


# Start FastAPI
app = FastAPI()

# Templates dir
templates = Jinja2Templates(directory="templates")

# Home
@app.get('/', response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
    
# Photo
@app.post("/photo/")
async def upload_photo(file: UploadFile = File(...)):
    # Save the file (Temp)
    response, file_location = photo.save(file)

    return {
        "title": file.filename,
        "saved": file_location,
        "response" :response
    }