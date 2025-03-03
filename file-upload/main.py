# main.py
from fastapi.responses import JSONResponse
from typing import Annotated
from fastapi import FastAPI, File, UploadFile
import shutil
import os
app = FastAPI()

# Directory to save uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
# Step 2: Define an endpoint to upload files
@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    # Step 3: Handle file upload and processing
    # Here, you can save, process, or analyze the uploaded file
    # For simplicity, we'll just return the file details
    return {"filename": file.filename}

# Step 4: Define an endpoint to download files (request files)
@app.get("/downloadfile/")
async def download_file(filename: str):
    # You can implement code to fetch and return the requested file
    # For now, we'll just return a placeholder response
    return JSONResponse(content={"message": f"Requested file: {filename}"})


@app.post('/files/')
async def create_files(file: Annotated[bytes, File()]):
    return {
        "file_size": len(file)
    }


@app.post('/upload_files/')
async def create_upload_files(files: list[UploadFile] = File(...)):
    images = []
    for file in files:
        images.append({
            "filename": file.filename,
            "bytes": str(file.file.read())[:30]
        })
    return {
        "images": images
    }


@app.post("/single-file-upload/")
async def single_upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    #print(file_location) #save files in database
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "saved_path": file_location}


@app.post("/multiple-files-upload/")
async def multiple_upload_files(files: list[UploadFile] = File(...)):
    saved_files = []
    
    for file in files:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        saved_files.append({"filename": file.filename, "saved_path": file_location})
    
    return {"files_uploaded": saved_files}
