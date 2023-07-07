import youtube_dl
import os

def whole_audio_to_file(url, output_path):
    title = url.split('/')[-2] + '_' + url.split('/')[-1]
    options = {
    'format': 'best',
    'outtmpl': f'{output_path}complete/{title}.mp3',  # Output filename template
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([url])
        