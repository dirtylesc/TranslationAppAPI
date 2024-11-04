from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from speech_to_text import getTextFromAudio

app = FastAPI()

@app.get("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
  audio_content = await file.read()
  
  data = getTextFromAudio(audio_content)
    
  return JSONResponse(content=data['content'], status_code=data['status_code'])
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)