from typing import Optional
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from contextlib import asynccontextmanager
import io
from pydantic import BaseModel
import uvicorn
import tempfile
import whisper
import utils
import aiofiles
from google.cloud import translate_v2 as translate
import os
import subprocess
import shutil
import whisper


class TranscribeRequest(BaseModel):
    fromLang: str
    video: UploadFile = File(...)

class TranscribeResponse(BaseModel):
    id: str
    captions: str

class TranslateRequest(BaseModel):
    id: str
    captions: str
    toLang: str

class TranslateResponse(BaseModel):
    id: str
    toLang: str
    translation: str



models = {}

if not os.path.exists('Wav2Lip'):
    import setup
    setup.setup_wav2lip()

@asynccontextmanager
async def lifespan(app: FastAPI):
    models["transriber"] = whisper.load_model("small")
    yield
    models.clear()

model = whisper.load_model("small")

app = FastAPI(lifespan=lifespan)

@app.get('/')
def index():
    return {'message': 'This is the homepage of the API '}


@app.post("/transcribe/")
async def transcribe(video: UploadFile = File(...), fromLang: str = Form(...)):
    video_bytes = await video.read()
    id = utils.generate_id()

    utils.video_to_audio(video_bytes, f"temp/{id}.wav")
    return TranscribeResponse(
        id=id,
        captions=utils.audio_to_text(models["transcriber"], f"temp/{id}.wav", fromLang),
    )

@app.post("/transcribe_text")
async def transcribe_text(video: UploadFile = File(...)):
    video_bytes = await video.read()

    id = utils.generate_id()
    with tempfile.TemporaryDirectory() as temp_dir:
        audio_path = os.path.join(temp_dir, f"{id}.wav")
        audio_bytes = utils.video_to_audio(video_bytes, audio_path)
        # audio_path.write(audio_bytes)
        # audio_path.seek(0)
    
        result = model.transcribe(audio=audio_path)

    return result["text"]
    

class TranslateRequest(BaseModel):
    text: str
    target_language: str


@app.post("/translate")
async def translate_fn(translationRequest: TranslateRequest):
    return TranslateResponse(
        id=translationRequest.id,
        toLang=translationRequest.toLang,
        translation=utils.translate(translationRequest.captions, translationRequest.toLang),
    )

    # with tempfile.d(delete=False, suffix=".wav") as temp_audio:
    #     temp_audio_path = temp_audio.name

    # video_to_audio(await video.read(), temp_audio_path)

    # # Return the video file as a response
    # return FileResponse(temp_audio_path, media_type="audio/wav", filename="output_audio.wav")

# class LipsyncRequest(BaseModel):
#     video: UploadFile = File(...)
#     translated_text: Optional[str] = ""

# TODO: WIP not yet tested due to package instabilities
@app.post("/synthesise")
async def synthesise(video: UploadFile = File(...), translated_text: Optional[str] = Form("")):

    try:
        id = utils.generate_id()
        video_bytes = await video.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            audio_path = temp_file.name
            audio_bytes = utils.video_to_audio(video_bytes, audio_path)
            print("starting TTS")
            await text_to_speech(translated_text, audio_path)
            print("finished TTS", audio_path)
            return FileResponse(audio_path, media_type="audio/wav", filename="output_adio")

            # return FileResponse()
            # os.chdir('Wav2Lip')
    
            # subprocess.run([
            #     'python', 'inference.py',
            #     '--checkpoint_path', 'checkpoints/wav2lip.pth',
            #     '--face', video_path,
            #     '--audio', audio_path,
            #     '--outfile', output_path
            # ], check=True)

            # return FileResponse(output_path, media_type='video/mp4', filename='result.mp4')
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # finally:
    #     if os.path.exists(audio_path):
    #         os.remove(audio_path)
        # os.chdir('..')



async def text_to_speech(text, audio_output_path):
    from gtts import gTTS
    try:
        tts = gTTS(text)
        tts.save(audio_output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
