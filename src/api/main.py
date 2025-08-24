from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
from src.api.speech_utils import transcribe_audio_file

app = FastAPI(title="Azure Speech-to-Text API")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        transcription = transcribe_audio_file(temp_path)
        return JSONResponse(content={"transcription": transcription})
    finally:
        os.remove(temp_path)