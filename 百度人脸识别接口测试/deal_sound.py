# coding=utf-8
import sys
from glob import glob
from pydub import AudioSegment
reload(sys) 
sys.setdefaultencoding('utf-8')






playlist_songs = [AudioSegment.from_mp3(mp3_file) for mp3_file in glob("*.m4a")]

first_song = playlist_songs.pop(0)

# let's just include the first 30 seconds of the first song (slicing
# is done by milliseconds)
beginning_of_song = first_song[:30*1000]

playlist = beginning_of_song
for song in playlist_songs:

    # We don't want an abrupt stop at the end, so let's do a 10 second crossfades
    playlist = playlist.append(song, crossfade=(10 * 1000))

# let's fade out the end of the last song
playlist = playlist.fade_out(30)

# hmm I wonder how long it is... ( len(audio_segment) returns milliseconds )
playlist_length = len(playlist) / (1000*60)

# lets save it!
out_f = open("%s_minute_playlist.mp3" % playlist_length, 'wb')

playlist.export(out_f, format='mp3')