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
