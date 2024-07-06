# from elevenlabs.client import ElevenLabs
# from elevenlabs import play
# import utils

# elClient = ElevenLabs(
#     api_key="102ce399cf07dc4356569a767fd8da11",
# )

# audio = elClient.generate(
#     text="Here's 5 tricks to make your.",
#     voice="Adam",
#     model="eleven_multilingual_v2"
# )
# play(audio)

# from deep_translator import GoogleTranslator

# translator = GoogleTranslator(source='auto')
# translator.target = "es"
# translated = translator.translate("keep it up, you are awesome")  # output -> Weiter so, du bist großartig
# print(translated)


# voice = elClient.clone(
#     name="Alex",
#     description="An old American male voice with a slight hoarseness in his throat. Perfect for news", # Optional
#     files=["temp/e3e6dfd0-35ee-4a4c-94fe-732015f82adf.wav"],
# )

# text = utils.audio_to_text()

# audio = elClient.generate(text="Hi! I'm a cloned voice!", voice=voice)

# play(audio)

import librosa
import soundfile as sf
import numpy
from pydub import AudioSegment

def change_audio_speed(file_path, speed=1.0):
    # y, sr = librosa.load(file_path)
    sound = AudioSegment.from_file(file_path)

    # y_fast = librosa.effects.time_stretch(y, speed)
    # new_file_path = f"modified_{file_path}"
    # sf.write(new_file_path, y_fast, sr)
    # return new_file_path

change_audio_speed("temp/2cabddd0-9a80-4b41-91e2-be9f36da0f57_generated.wav", 1.5)