from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
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
    # # Save the uploaded video file to a temporary file
    with open("temp_video.mp4", "wb") as buffer:
        buffer.write(await video.read())

    # Return the video file as a response
    return FileResponse("temp_video.mp4", media_type="video/mp4")
    # with tempfile.d(delete=False, suffix=".wav") as temp_audio:
    #     temp_audio_path = temp_audio.name

    # video_to_audio(await video.read(), temp_audio_path)

    # # Return the video file as a response
    # return FileResponse(temp_audio_path, media_type="audio/wav", filename="output_audio.wav")