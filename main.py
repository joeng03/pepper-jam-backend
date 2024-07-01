from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from contextlib import asynccontextmanager
import io
import uvicorn
import tempfile
import whisper
from utils import video_to_audio

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
async def transribe(video: UploadFile = File(...)):
    video_bytes = await video.read()

    # Convert video bytes to audio bytes
    audio_bytes = video_to_audio(video_bytes)

    # Return the audio file as a streaming response
    return StreamingResponse(io.BytesIO(audio_bytes), media_type="audio/wav")


    

    # with tempfile.d(delete=False, suffix=".wav") as temp_audio:
    #     temp_audio_path = temp_audio.name

    # video_to_audio(await video.read(), temp_audio_path)

    # # Return the video file as a response
    # return FileResponse(temp_audio_path, media_type="audio/wav", filename="output_audio.wav")