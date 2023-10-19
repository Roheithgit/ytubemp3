from flask import Flask, request, send_file
from pytube import YouTube
import os
from moviepy.editor import VideoFileClip

app = Flask(__name__)

@app.route('/')
def defaultpg():
    return 'Hello Universe'

@app.route('/download/<yturl>')
def download_video(yturl):
    def download(link, download_path):
        try:
            youtube_object = YouTube(f"https://www.youtube.com/watch?v={link}")
            video_stream = youtube_object.streams.get_highest_resolution()
            video_stream.download(output_path=download_path)
            return os.path.join(download_path, youtube_object.title + ".mp4")
        except Exception as e:
            return f"An error has occurred: {str(e)}"

    download_path = "your_download_directory"  # Replace with your desired download directory
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    video_path = download(yturl, download_path)

    # Access youtube_object.title outside the try block
    youtube_object = None
    try:
        youtube_object = YouTube(f"https://www.youtube.com/watch?v={yturl}")
    except Exception as e:
        return f"An error has occurred: {str(e)}"

    audio_output_path = os.path.join(download_path, youtube_object.title + ".mp3")

    # Extract audio and save it as an MP3 file
    clip = VideoFileClip(video_path)
    audio_clip = clip.audio
    audio_clip.write_audiofile(audio_output_path)

    # Send the audio file as an attachment with the specified filename
    return send_file(audio_output_path, as_attachment=True)

if __name__ == '__main__':
    app.run()
