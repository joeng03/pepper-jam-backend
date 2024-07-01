import ffmpeg
import io


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
    input_stream = io.BytesIO(input_bytes)
    output_stream = io.BytesIO()
    
    process = (
        ffmpeg
        .input('pipe:0')
        .output('pipe:1', format='wav')
        .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
    )

    stdout, _ = process.communicate(input=input_stream.read())
    output_stream.write(stdout)
    output_stream.seek(0)
    return output_stream.read()