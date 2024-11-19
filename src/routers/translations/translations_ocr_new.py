from src.utils.base import preprocess_image, extract_word_images
from src.utils.model import OCRModel
import cv2
import numpy as np
from PIL import Image
import io
from fastapi import HTTPException, File, UploadFile,APIRouter
from fastapi.responses import JSONResponse, FileResponse
import os
# Load model và configs (giữ nguyên như trong code của bạn)
try:
    from mltu.configs import BaseModelConfigs
    configs = BaseModelConfigs.load("src/data/configs.yaml")
    model = OCRModel(model_path="src/data/model.onnx", char_list=configs.vocab)
except Exception as e:
    raise Exception(f"Error loading model or configs: {e}")

tags = ["translations"]
router = APIRouter(
    responses={404: {"description": "Not found"},
               500: {"description": "Server error"}},
)

# Đường dẫn thư mục lưu ảnh
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
@router.post("/ocr",tags=tags)
async def predict_text(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        # Lưu file vào thư mục 'uploads/'
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            f.write(contents)

        predicted_text = model.predict(contents)

        # Xử lý ảnh để vẽ bounding boxes
        image = Image.open(io.BytesIO(contents))
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Chuyển từ RGB sang BGR

        binary = preprocess_image(contents)
        word_images = extract_word_images(binary)

        for _, bbox in word_images:
            x, y, w, h = bbox
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Lưu ảnh đã vẽ bounding boxes
        output_path = os.path.join(OUTPUT_FOLDER, "output_" + file.filename)
        cv2.imwrite(output_path, image)

        return JSONResponse(content={"text": predicted_text, "output_image_path": output_path})

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Thêm route để trả về ảnh đã xử lý
@router.get("/output/{image_name}")
async def get_output_image(image_name: str):
    image_path = os.path.join(OUTPUT_FOLDER, image_name)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)

