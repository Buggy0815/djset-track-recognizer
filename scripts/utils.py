import pandas as pd
from ShazamAPI import Shazam
import youtube_dl
import os
from pydub import AudioSegment
import io
from multiprocessing import Pool

def get_tracklist_of_url(url, output_path):
    '''
    main function
    '''
    title = url.split('/')[-2] + '_' + url.split('/')[-1]
    whole_audio_to_file(url, output_path) #download and save audio
    audio = AudioSegment.from_file(f'{output_path}complete/{title}.mp3', format='mp3') #load audio
    chunks = chunking(audio)
    tracks = get_tracks(chunks)
    df = tracks_to_df(tracks)
    return df
    
def tracks_to_df(tracks):
    df = pd.DataFrame(tracks)
    df = df.dropna()
    df = df.drop_duplicates()
    df['artist'] = df[0].apply(lambda x: x[0]).copy()
    df['track'] = df[0].apply(lambda x: x[1]).copy()
    df = df.drop(columns=[0])
    df = df.drop_duplicates().rename(columns = {0:'artist', 1:'track'})
    return df

def get_tracks(chunks):
    tracks = []
    with Pool() as pool:
        # call the same function with different data in parallel
        for result in pool.map(get_artist_title, chunks):
            # report the value to show progress
            tracks.append(result)
    return tracks
    
def chunking(audio):
    chunks = []
    chunk_length_ms = 30*1000   # 30-second chunks
    delay = 4 *60*1000            # every 2 minutes
    count = 40*1000             # starting at 40 seconds

    while True:
        start_time = count
        end_time = count + chunk_length_ms

        # Extract the desired chunk from the audio
        audio_chunk = audio[start_time:end_time]

        # Export the audio chunk as an MP3 file to a BytesIO object
        audio_file = io.BytesIO()
        audio_chunk.export(audio_file, format='mp3')

        # Read the audio data from the BytesIO object
        audio_data = audio_file.getvalue()

        # Add the audio data to the list
        chunks.append(audio_data)

        count = count + chunk_length_ms + delay
        if count + chunk_length_ms > len(audio):
            break          
    return chunks
    
def whole_audio_to_file(url, output_path):
    title = url.split('/')[-2] + '_' + url.split('/')[-1]
    options = {
    'format': 'best',
    'outtmpl': f'{output_path}complete/{title}.mp3',  # Output filename template
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([url])
    print('downloaded')

def get_artist_title(file):
    '''
    returns artist,track
    '''
    shazam = Shazam(file)
    recognize_generator = shazam.recognizeSong()
    
    # Set the desired number of songs to recognize
    num_songs_to_recognize = 1
    songs_recognized = 0
    
    while songs_recognized < num_songs_to_recognize:
        try:
            song_info = next(recognize_generator)
            #print(song_info)
            songs_recognized += 1
            return song_info[1]['track']['subtitle'], song_info[1]['track']['title']
        except (StopIteration, KeyError):
            break