from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from contextlib import asynccontextmanager
import io
from pydantic import BaseModel
import uvicorn
import tempfile
import whisper
from utils import video_to_audio
import aiofiles
from google.cloud import translate_v2 as translate

models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    models["transriber"] = whisper.load_model("small")
    yield
    models.clear()

app = FastAPI(lifespan=lifespan)


@app.get('/')
def index():
    return {'message': 'This is the homepage of the API '}


@app.post("/transcribe/")
async def transcribe(video: UploadFile = File(...)):
    video_bytes = await video.read()

    # Convert video bytes to audio bytes
    audio_bytes = video_to_audio(video_bytes)

    # Save audio bytes to a file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio.seek(0)

    # Return the audio file as a streaming response
    return FileResponse(temp_audio.name, media_type="audio/wav", filename="output_audio.wav")

class TranslateRequest(BaseModel):
    text: str
    target_language: str


@app.post("/translate")
async def translate_fn(translationRequest: TranslateRequest):
    translate_client = translate.Client()
    
    text = translationRequest.text
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    result = translate_client.translate(text, target_language=translationRequest.target_language)
    
    return result['translatedText']


    # with tempfile.d(delete=False, suffix=".wav") as temp_audio:
    #     temp_audio_path = temp_audio.name

    # video_to_audio(await video.read(), temp_audio_path)

    # # Return the video file as a response
    # return FileResponse(temp_audio_path, media_type="audio/wav", filename="output_audio.wav")