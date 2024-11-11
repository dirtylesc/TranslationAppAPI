from fastapi import File, UploadFile, APIRouter, HTTPException
from PIL import Image
import io
import easyocr

reader = easyocr.Reader(['en', 'vi'])

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
    except Exception as e:
        raise HTTPException(status_code=500, detail="Không thể đọc ảnh")
    try:
        result = reader.readtext(image)
        text_result = " ".join([text for _, text, _ in result])
    except Exception as e:
        raise HTTPException(status_code=500, detail="Lỗi khi nhận diện văn bản")
    return {"text": text_result}