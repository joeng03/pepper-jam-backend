import ffmpeg
import io
from TTS.api import TTS
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)


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


def video_to_audio(input_bytes: bytes) -> bytes:
    # Use ffmpeg to convert video bytes to audio bytes
    process = (
        ffmpeg
        .input('pipe:0')
        .output('pipe:1', format='wav')
        .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
    )

    stdout, _ = process.communicate(input=input_bytes)
    if process.returncode != 0:
        raise ffmpeg.Error('ffmpeg', process.returncode, process.stderr)
    
    return stdout

def text_to_audio(text: str, language: str, speaker_wav: str):
    tts.tts_to_file(text=text, language=language, speaker_wav=speaker_wav, file_path="temp/output.wav")
    
