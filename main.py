# FastApi modules
from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile

# HTML response
from fastapi.responses import HTMLResponse

# Shutil for files
import shutil

app = FastAPI()

# Home
@app.get('/')
async def get_home():
    content = """
    <html>
        <body>
            <h3>Upload a photo</h3>
            <form action="/photo/" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=content)
    
# Photo
@app.post("/photo/")
async def upload_photo(file: UploadFile = File(...)):
    # Guardar el archivo en el servidor
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {"info": f"file '{file.filename}' saved at '{file_location}'"}