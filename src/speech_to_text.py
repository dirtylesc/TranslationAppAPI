import speech_recognition as sr
from pydub import AudioSegment
import io


async def getTextFromAudio(audio_content: bytes):
  # Chuyển đổi tệp âm thanh sang định dạng WAV nếu cần
  audio_segment = AudioSegment.from_file(io.BytesIO(audio_content))
  wav_io = io.BytesIO()
  audio_segment.export(wav_io, format="wav")
  wav_io.seek(0)
  
  # Nhận diện giọng nói
  recognizer = sr.Recognizer()
  with sr.AudioFile(wav_io) as source:
      audio_data = recognizer.record(source)
      try:
          text = recognizer.recognize_google(audio_data)
          return {"content": text, "status_code": 200}
      except sr.UnknownValueError:
          return {"content": {"error": "Could not understand audio"}, "status_code": 400}
      except sr.RequestError as e:
          return {"content": {"error": f"Could not request results from Google Speech Recognition service; {e}"}, "status_code": 400}