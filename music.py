

from pathlib import Path

import os
import sys 
import glob




class Music():
    def __init__(self):
        self.MUSIC_DIR = os.path.abspath("music/")

        self.STANDARD_SCALE = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        self.trans_scale = self.STANDARD_SCALE#['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

        self.LYRICS_KEY = "lyrics:"
        self.CHORD_KEY = "chord_:"

    def MusicList(self,artist_name = None):
        artist_dir = self.MUSIC_DIR + '/' + artist_name 

        sample_list = glob.glob(os.path.join(artist_dir,'*'))
        music_list = []

        for file_str in sample_list:
            if os.path.isfile(file_str):
                    file_name = Path(file_str).stem
                    music_list.append(file_name)

        return music_list

    def GetMusicinfo(self, artist_name, music_name):
        self.lyrics_list = []
        self.chord_list = []

        music_file = self.MUSIC_DIR+'/'+artist_name+'/'+music_name+'.txt'

        with open(music_file,encoding="utf-8") as tf:

            for i, line in enumerate(tf):

                if line.find(self.LYRICS_KEY) >= 0:
                    self.lyrics_list.append(line.strip('lyrics:,\n'))
                elif line.find(self.CHORD_KEY) >= 0:
                    self.chord_list.append(line.strip('chord_:,\n'))

        print(self.lyrics_list)
        print(self.chord_list)

    def GetChord(self,num):
        return self.chord_list[num]

    def GetLyrics(self,num):
        return self.lyrics_list[num]
