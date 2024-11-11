from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile, APIRouter, HTTPException
from PIL import Image
import pytesseract
import io
tags = ["translations"]
router = APIRouter(
    responses={404: {"description": "Not found"},
               500: {"description": "Server error"}},
)

@router.post("/img2text", tags=tags)
async def image2text(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(image, lang='eng')
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the image: {str(e)}")