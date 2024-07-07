from typing import Optional
from fastapi import FastAPI, APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import io
from pydantic import BaseModel
import uvicorn
import tempfile
import whisper
import utils
import aiofiles
import os
import subprocess
import shutil
from elevenlabs import save





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

class GenerateRequest(BaseModel):
    id: str
    toLang: str
    translation: str

class GenerateResponse(BaseModel):
    id: str
    url: str



models = {}

if not os.path.exists('Wav2Lip'):
    import setup
    setup.setup_wav2lip()

@asynccontextmanager
async def lifespan(app: FastAPI):
    models["transriber"] = whisper.load_model("small")
    yield
    models.clear()

origins = [
    "http://localhost:3000"
]

api_router = APIRouter(prefix="/api")
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@api_router.get('/')
def index():
# List of allowed origins

    return {'message': 'This is the homepage of the API '}




@api_router.post("/upload")
async def transcribe(video: UploadFile = File(...), fromLang: str = Form("...")):
    video_bytes = await video.read()

    id = utils.generate_id()
    
    audio_file_path = f"temp/{id}.wav"
    video_file_path = f"temp/{id}.mp4"

    with open(video_file_path, "wb") as video_file:
        video_file.write(video_bytes)

    utils.video_to_audio(video_bytes, audio_file_path)
    result = models["transriber"].transcribe(audio=audio_file_path, language=fromLang)

    print(result["text"])
    return TranscribeResponse(
        id=id,
        captions=result["text"],
    )
    

@api_router.post("/translate")
async def translate_fn(translationRequest: TranslateRequest):
    id = utils.generate_id()
    return TranslateResponse(
        id=id,
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


class TestResponse(BaseModel):
    response: str

@api_router.get("/test")
async def test():
    # return TestResponse(
    #     response="Hello World"
    # )
    return FileResponse("temp/8d573a6e-a864-4cb9-99e0-d31c43889d66_generated.wav", media_type="audio/wav", filename="output_audio.wav")

@api_router.post("/generate")
async def generate(generateRequest: GenerateRequest):
    id = generateRequest.id
    translated_text = generateRequest.translation
    toLang = generateRequest.toLang
    try:
        video_file_path = f"temp/{id}.mp4"
        audio_file_path = f"temp/{id}.wav"

        video = None
        audio = None
        if os.path.isfile(video_file_path):
            video = open(video_file_path, "rb")
        if os.path.isfile(audio_file_path):
            audio = open(audio_file_path, "rb")

        if video is None:
            raise HTTPException(status_code=404, detail="Video not found")
        if audio is None:
            raise HTTPException(status_code=404, detail="Audio not found")

        generatedAudioPath = f"temp/{id}_generated.wav"
        generatedVideoPath = f"temp/{id}_generated.mp4"
        audioBytes = utils.generateVoice(id=id, text=translated_text)

        save(audioBytes, generatedAudioPath)

        utils.replace_audio(video_file_path, generatedAudioPath, generatedVideoPath)

        return FileResponse(
            generatedVideoPath, media_type="video/mp4", filename="output_video.mp4"
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=4, detail=str(e))


async def text_to_speech(text, audio_output_path):
    from gtts import gTTS
    try:
        tts = gTTS(text)
        tts.save(audio_output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
