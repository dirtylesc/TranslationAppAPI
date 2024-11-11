from fastapi import APIRouter

from src.routers.translations import translations_stt
from src.routers.translations import  translations_ocr
prefix = "/api/v1"

router = APIRouter(
    prefix=prefix,
    responses={
        404: {"error": "Not found"},
        500: {"server_error": "Internal server error"}
    }
)

router.include_router(translations_stt.router)
router.include_router(translations_ocr.router)