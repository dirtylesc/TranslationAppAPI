import sys

from fastapi import File, UploadFile, HTTPException, APIRouter
from fastapi.responses import JSONResponse
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment

tags = ["translations"]
router = APIRouter(
    responses={404: {"description": "Not found"},
               500: {"description": "Server error"}},
)

@router.post("/upload-audio", tags=tags)
async def transcribe(file: UploadFile = File(...), language: str = "en"):
    if not file.filename.endswith(".wav"):
        audio_data = await file.read()
        audio_file = BytesIO(audio_data)
        try:
            audio = AudioSegment.from_file(audio_file)
            wav_audio = BytesIO()
            audio.export(wav_audio, format="wav")
            wav_audio.seek(0)
            audio_file = wav_audio
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Lỗi chuyển đổi âm thanh: {str(e)}")

    recognizer = sr.Recognizer()
    

    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language=language)
        return JSONResponse(content={"transcription": text})
    except sr.UnknownValueError:
        raise HTTPException(status_code=422, detail="Không thể nhận diện giọng nói từ tệp âm thanh")
    except sr.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Lỗi kết nối với dịch vụ nhận diện: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Đã xảy ra lỗi không mong muốn: {str(e)}")