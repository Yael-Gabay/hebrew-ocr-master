from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.openapi.docs import get_swagger_ui_html
from Split_Img import perform_ocr
import cv2
import numpy as np
import requests
from PIL import Image
import pytesseract
import io

app = FastAPI()

class ImageResponse(BaseModel):
    message: str

def read_image(file) -> np.ndarray:
    img = Image.open(io.BytesIO(file))
    return np.array(img)

router = APIRouter()

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), type: str = "text") -> str:
    try:
        file_path = f"uploads/{file.filename}"
        print(file_path)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        perform_ocr(file_path)
        
        print(file_path)
        if type == "text":
            res = pytesseract.image_to_string(Image.open(file_path), lang="heb")
        else:
            res = requests.get('http://localhost:8010/predict_sentnece').json()

        return res
    

    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.get("/")
async def read_root():
    return {"message": "Welcome to the Image API."}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Image API")

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
