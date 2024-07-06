import ffmpeg
import io
# from TTS.api import TTS
import torch
# from googletrans import Translator
from deep_translator import GoogleTranslator
import uuid
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings, play

elClient = ElevenLabs(
    api_key="",
)

device = "cuda" if torch.cuda.is_available() else "cpu"
# translator = GoogleTranslator(source='auto', target='en')
translator = GoogleTranslator(source='auto')

# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# def video_to_audio(input_file, output_file_path):
#     # stream = ffmpeg.input(input_file)
#     # stream = ffmpeg.output(stream, output_file, ab='160k', ac=2, ar=44100, vn=None)

#     # try:
#     #     ffmpeg.run(stream, capture_stderr=True)  # Capture stderr output in case of errors
#     #     print("Conversion complete!")
#     # except ffmpeg.Error as e:
#     #     print(e.stderr.decode())  # Print the stderr output for debugging

#     (
#         ffmpeg
#         .input('pipe:0')
#         .output(output_file_path)
#         .run(input=input_file)
#     )

def generate_id() -> str:
    return str(uuid.uuid4())

def video_to_audio(input_bytes: bytes, output_file_path: str):
    # Use ffmpeg to convert video bytes to audio bytes

    process = (
        ffmpeg
        .input('pipe:0')
        .output(output_file_path, format='wav')
        .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
    )

    stdout, stderr = process.communicate(input=input_bytes)
    if process.returncode != 0:
        print("STDERR: ", stderr)
        raise ffmpeg.Error('ffmpeg', process.returncode, stderr)

def audio_to_text(model, audio_file_path: str, language: str) -> str:
    result = model.transcribe(audio=audio_file_path, language=language)
    return result["text"]


def translate(text: str, target_language: str):
    translator.target = target_language
    translated = translator.translate(text)  # output -> Weiter so
    return translated

def generateVoice(id: str, text: str):
    voice = elClient.clone(
        name=id,
        description="",
        files=[f"temp/{id}.wav"],    
    )
    
    audio = elClient.generate(text=text, voice=voice)
    return audio

# def text_to_audio(text: str, language: str, speaker_wav: str):
    # tts.tts_to_file(text=text, language=language, speaker_wav=speaker_wav, file_path="temp/output.wav")
    # 

