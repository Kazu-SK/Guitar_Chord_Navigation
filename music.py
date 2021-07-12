

from pathlib import Path

import os
import sys 
import glob




class Music():


    def __init__(self):

        self.Config()

        self.trans_scale = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']


    def Config(self):
        self.MUSIC_DIR = os.path.abspath("music/")

        self.STANDARD_SCALE = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

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

    def ArtistList(self):
        artist_list = os.listdir(self.MUSIC_DIR)

        return artist_list


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


        self.lyrics_end_num = len(self.lyrics_list)-1

        tf.close()


    def TransposeScale(self,trans_code):

        if trans_code == 'plus':

            tmp = self.trans_scale[0]  

            for i in range(len(self.trans_scale)-1):
                self.trans_scale[i] = self.trans_scale[i+1]

            self.trans_scale[len(self.trans_scale)-1] = tmp

        elif trans_code == 'minus':
            tmp = self.trans_scale[len(self.trans_scale)-1]  

            for i in range(len(self.trans_scale)-1, 0, -1):
               self.trans_scale[i] = self.trans_scale[i-1]

            self.trans_scale[0] = tmp

        else:
            print('error TransposeChord')


    def TransposeChord(self,current_chord):  

        target_list = []
        target_str = []
        trans_chord = []


        if current_chord[len(current_chord)-1] == '#':
            loop_count = len(current_chord)


        for i in range(len(current_chord)):

            if current_chord[i] in self.STANDARD_SCALE:

                if i != len(current_chord)-1: 
                    if current_chord[i+1] == '#':
                        target_list.append(current_chord[i])
                        target_list.append(current_chord[i+1])
                    else:
                        target_list.append(current_chord[i])
                else:
                    target_list.append(current_chord[i])


                target_str = "".join(target_list)
                trans_num = self.STANDARD_SCALE.index(target_str)

                trans_chord.append(self.trans_scale[trans_num])

                target_list = []

            elif current_chord[i] == '#':
                continue
            else:
                trans_chord.append(current_chord[i])


        trans_chord = "".join(trans_chord)


        return trans_chord


    def GetLyricsEndnum(self):
        return self.lyrics_end_num

    def GetChord(self,num):
        return "".join(self.chord_list[num])

    def GetLyrics(self,num):
        return "".join(self.lyrics_list[num])
