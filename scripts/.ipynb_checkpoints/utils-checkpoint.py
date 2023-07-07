from ShazamAPI import Shazam

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