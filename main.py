from fastapi import FastAPI, File, UploadFile
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


class TranscribeRequest(BaseModel):
    video: UploadFile = File(...)
    language: str

class TranslateRequest(BaseModel):
    text: str
    target_language: str


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
async def transcribe(transcribeRequest: TranscribeRequest):
    video_bytes = await transcribeRequest.video.read()
    id = utils.generate_id()

    utils.video_to_audio(video_bytes, f"temp/{id}.wav")
    return utils.audio_to_text(models["transriber"], f"temp/{id}.wav", transcribeRequest.language)


@app.post("/translate")
async def translate_fn(translationRequest: TranslateRequest):
    return utils.translate(translationRequest.text, translationRequest.target_language)


    # with tempfile.d(delete=False, suffix=".wav") as temp_audio:
    #     temp_audio_path = temp_audio.name

    # video_to_audio(await video.read(), temp_audio_path)

    # # Return the video file as a response
    # return FileResponse(temp_audio_path, media_type="audio/wav", filename="output_audio.wav")
