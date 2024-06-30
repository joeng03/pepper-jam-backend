from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import uvicorn
import pickle
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
async def upload_video(video: UploadFile = File(...)):
    video_to_audio("temp_video.mp4", video.file)

    # Return the video file as a response
    return FileResponse("temp_video.mp4", media_type="video/mp4")
