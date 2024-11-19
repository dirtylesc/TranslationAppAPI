from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from mltu.configs import BaseModelConfigs
from src.utils.model import OCRModel

try:
    configs = BaseModelConfigs.load("src/data/configs.yaml")
    model = OCRModel(model_path="src/data/model.onnx", char_list=configs.vocab)
except Exception as e:
    raise Exception(f"Error loading model or configs: {e}")

tags = ["translations"]
router = APIRouter(
    responses={404: {"description": "Not found"},
               500: {"description": "Server error"}},
)

@router.post("/ocr",tags=tags)
async def predict_text(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        predicted_text = model.predict(contents)
        return JSONResponse(content={"text": predicted_text})
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

