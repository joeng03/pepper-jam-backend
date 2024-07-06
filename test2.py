from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from moviepy.video import fx
import pyrubberband as pyrb


# def replace_audio(video_path, audio_path, output_path):
#     # Load the video
#     video = VideoFileClip(video_path)
    
#     # Load the new audio
#     new_audio = AudioFileClip(audio_path)
    
#     # Set the new audio to the videoAudio
#     new_audio_clip = CompositeAudioClip([new_audio])
#     video.audio = new_audio_clip
#     # video_with_new_audio = video.set_audio(new_audio)
    
#     # Write the result to a file
#     video.write_videofile(output_path, codec='libx264', audio_codec='aac')


# def replace_audio(video_path, audio_path, output_path):
#     # Load the video
#     video = VideoFileClip(video_path)
    
#     # Load the new audio
#     new_audio = AudioFileClip(audio_path)
    
#     # Calculate the ratio of the video duration to the audio duration
#     duration_ratio = new_audio.duration / video.duration
    
#     # Adjust the audio speed to match the video duration
#     adjusted_audio = new_audio.fx(fx.all.speedx, factor=duration_ratio)
    
#     # Set the new audio to the video
#     new_audio_clip = CompositeAudioClip([adjusted_audio])
#     video.audio = new_audio_clip
    
#     # Write the result to a file
#     video.write_videofile(output_path, codec='libx264', audio_codec='aac')


from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import os
import soundfile as sf

def replace_audio(video_path, audio_path, output_path):
    # Load the video
    video = VideoFileClip(video_path)

    y, sr = sf.read(audio_path)

    # Calculate the duration ratio and adjust the audio speed
    duration_ratio = video.duration / AudioFileClip(audio_path).duration
    # time_stretch(audio_path, temp_audio_path, speed=duration_ratio)
    y_stretch = pyrb.time_stretch(y, sr, duration_ratio)
    stretched_audio_path = f"temp/{id}_generated.wav"
    sf.write(stretched_audio_path, y_stretch, sr, format='wav')


    # Load the adjusted audio
    new_audio = AudioFileClip(stretched_audio_path)
    
    # Set the new audio to the video
    new_audio_clip = CompositeAudioClip([new_audio])
    video.audio = new_audio_clip
    
    # Write the result to a file
    video.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # Clean up the temporary file
    os.remove(stretched_audio_path)

filename = f"temp/2cabddd0-9a80-4b41-91e2-be9f36da0f57"

video = f"{filename}.mp4"
audio = f"{filename}_generated.wav"

output = "temp/output.mp4"

replace_audio(video, audio, output)



# import sys
# from pydub import AudioSegment
# #sound = AudioSegment.from_file("deviprasadgharpehai.mp3")
# sound = AudioSegment.from_mp3(sys.argv[1])
# sound.export("file.wav", format="wav")

# print(sys.argv[1])

# import soundfile as sf
# import pyrubberband as pyrb
# y, sr = sf.read("file.wav")
# # Play back at extra low speed
# y_stretch = pyrb.time_stretch(y, sr, 0.5)
# # Play back extra low tones
# y_shift = pyrb.pitch_shift(y, sr, 0.5)
# sf.write("analyzed_filepathX5.wav", y_stretch, sr, format='wav')

# sound = AudioSegment.from_wav("analyzed_filepathX5.wav")
# sound.export("analyzed_filepathX5.mp3", format="mp3")

# # Play back at low speed
# y_stretch = pyrb.time_stretch(y, sr, 0.75)
# # Play back at low tones
# y_shift = pyrb.pitch_shift(y, sr, 0.75)
# sf.write("analyzed_filepathX75.wav", y_stretch, sr, format='wav')

# sound = AudioSegment.from_wav("analyzed_filepathX75.wav")
# sound.export("analyzed_filepathX75.mp3", format="mp3")

# # Play back at 1.5X speed
# y_stretch = pyrb.time_stretch(y, sr, 1.5)
# # Play back two 1.5x tones
# y_shift = pyrb.pitch_shift(y, sr, 1.5)
# sf.write("analyzed_filepathX105.wav", y_stretch, sr, format='wav')

# sound = AudioSegment.from_wav("analyzed_filepathX105.wav")
# sound.export("analyzed_filepathX105.mp3", format="mp3")

# # Play back at same speed
# y_stretch = pyrb.time_stretch(y, sr, 1)
# # Play back two smae-tones
# y_shift = pyrb.pitch_shift(y, sr, 1)
# sf.write("analyzed_filepathXnormal.wav", y_stretch, sr, format='wav')

# sound = AudioSegment.from_wav("analyzed_filepathXnormal.wav")
# sound.export("analyzed_filepathXnormal.mp3", format="mp3")
