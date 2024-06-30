import ffmpeg


def video_to_audio(input_file, output_file):
    stream = ffmpeg.input(input_file)
    stream = ffmpeg.output(stream, output_file, ab='160k', ac=2, ar=44100, vn=None)

    try:
        ffmpeg.run(stream, capture_stderr=True)  # Capture stderr output in case of errors
        print("Conversion complete!")
    except ffmpeg.Error as e:
        print(e.stderr.decode())  # Print the stderr output for debugging