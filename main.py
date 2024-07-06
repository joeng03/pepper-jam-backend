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

model = whisper.load_model("small")

app = FastAPI(lifespan=lifespan)

@app.get('/')
def index():
    return {'message': 'This is the homepage of the API '}




@app.post("/transcribe")
async def transcribe(video: UploadFile = File(...)):
    video_bytes = await video.read()

    id = utils.generate_id()
    
    audio_file_path = f"temp/{id}.wav"
    video_file_path = f"temp/{id}.mp4"

    with open(video_file_path, "wb") as video_file:
        video_file.write(video_bytes)

    utils.video_to_audio(video_bytes, audio_file_path)
    result = model.transcribe(audio=audio_file_path)

    return TranscribeResponse(
        id=id,
        captions=result["text"]
    )
    

@app.post("/translate")
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

@app.post("/generate")
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
        audioBytes = utils.generateVoice(id=id, text=translated_text)

        save(audioBytes, generatedAudioPath)
        
        # print("finished TTS", audio_path)
        # return FileResponse(path=, media_type="audio/wav", filename="output_audio.wav")

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
        raise HTTPException(status_code=4, detail=str(e))
    
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
