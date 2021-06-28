


from tkinter import *
from tkinter import ttk

from enum import Enum

import threading


import os
import music as m


class Sound(Enum):
    NONE_STATUS = 0
    TEST_STATUS = 1
    PLAY_STATUS = 2


class Playback(Enum):
    #playback
    START_POSITION = 0 
    MIDWAY_POSITION = 1 
    END_POSITION = 2 


class MainWindow(ttk.Frame):
    def __init__(self,master = None):
        master.title('lyrics_and_chord')
        master["bg"] = "black"

        frame_style = ttk.Style()
        frame_style.configure('s.TFrame',background='black')
        self.main_frame = super().__init__(master,style='s.TFrame')

        self.grid()

        self.music_obj = m.Music()

        #music lyrics and chord init

        self.artist_list = self.music_obj.ArtistList()

        self.artist_name = '/' + self.artist_list[0]
        self.music_list = self.music_obj.MusicList(self.artist_name)
        self.music_name = self.music_list[0]
        self.music_obj.GetMusicinfo(self.artist_name,self.music_name)
        self.display_line_upper = 0
        self.display_line_lower = 1

        self.chord_upper = self.music_obj.GetChord(self.display_line_upper)
        self.chord_lower = self.music_obj.GetChord(self.display_line_lower)
        self.lyrics_upper = self.music_obj.GetLyrics(self.display_line_upper)
        self.lyrics_lower = self.music_obj.GetLyrics(self.display_line_lower)

        print(self.lyrics_upper)
        print(self.lyrics_lower)
        print(self.chord_upper)
        print(self.chord_lower)

        self.yellow_display_num = 0


        self.INTERVAL_LIST = [1,2,3,4]

        #Metronome
        import pygame.mixer
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

        self.level_tempo = 40 
        self.level_volume = 0
        self.button_status = False 
        self.volume_on = True 
        self.beat_list = [2,3,4,6]
        self.beat_count = 0
        self.sound_status = Sound.NONE_STATUS 
        self.playback_status = Playback.START_POSITION 

        self.high_sound = pygame.mixer.Sound("sound/piltu3.wav")
        self.low_sound = pygame.mixer.Sound("sound/piltu4.wav")

        self.working_app = True

        self.high_sound.set_volume(1)
        self.low_sound.set_volume(1)


        self.lyrics_num = [0, 1]
        

        for i in range(2,7):
            master.grid_columnconfigure(i,weight=1)

        master.grid_columnconfigure(0,weight=1)

        for j in range(10):
            master.grid_rowconfigure(j,weight=1)
    

    def SelectArtist(self,event):

        for i in self.lb_artist.curselection():
            self.artist_name = self.lb_artist.get(i)

        #print(self.artist_name)


        self.music_list = self.music_obj.MusicList(self.artist_name)

        #print('music_list')
        #print(self.music_list)

        #v2 = StringVar(value=self.music_list) 
        self.lb_music.configure(listvariable = StringVar(value=self.music_list)) 
        self.lb_music.update()


    def SelectMusic(self):
        for i in self.lb_music.curselection():
            self.music_name = self.lb_music.get(i)

        #print(self.artist_name)
        #print(self.music_name)

        self.music_obj.GetMusicinfo(self.artist_name,self.music_name)

        self.display_line_upper = 0
        self.display_line_lower = 1


        self.label_music.configure(text = self.music_name, foreground="white",background="black")
        self.label_artist.configure(text = self.artist_name.replace('/',''), foreground="white",background="black")
        self.label_music.update()
        self.label_artist.update()

        #print(self.artist_name)


        self.lyrics_num = [0, 1]
        self.yellow_display_num = 0


        self.DisplayChord()
        self.DisplayLyrics()

    '''
    def Template(self,event):
        print('tmp')
        '''


    def DisplayChord(self):

        '''
        self.chord_upper = self.music_obj.GetChord(self.display_line_upper)
        self.label_chord_upper.configure(text = self.chord_upper, background="black")
        self.label_chord_upper.update()

        self.chord_lower = self.music_obj.GetChord(self.display_line_lower)
        self.label_chord_lower.configure(text = self.chord_lower, background="black")
        self.label_chord_lower.update()
        '''

        if self.display_line_upper == self.yellow_display_num:
            self.chord_upper = self.music_obj.GetChord(self.display_line_upper)
            self.chord_upper = self.music_obj.TransposeChord(self.chord_upper)
            self.label_chord_upper.configure(text = self.chord_upper, foreground="yellow",background="black")
            self.label_chord_upper.update()

            self.chord_lower = self.music_obj.GetChord(self.display_line_lower)
            self.chord_lower = self.music_obj.TransposeChord(self.chord_lower)
            self.label_chord_lower.configure(text = self.chord_lower, foreground="white",background="black")
            self.label_chord_lower.update()
        else:
            self.chord_upper = self.music_obj.GetChord(self.display_line_upper)
            self.chord_upper = self.music_obj.TransposeChord(self.chord_upper)
            self.label_chord_upper.configure(text = self.chord_upper, foreground="white",background="black")
            self.label_chord_upper.update()

            self.chord_lower = self.music_obj.GetChord(self.display_line_lower)
            self.chord_lower = self.music_obj.TransposeChord(self.chord_lower)
            self.label_chord_lower.configure(text = self.chord_lower, foreground="yellow",background="black")
            self.label_chord_lower.update()


    def DisplayLyrics(self):

        '''

        self.lyrics_upper = self.music_obj.GetLyrics(self.display_line_upper)
        self.label_lyrics_upper.configure(text = self.lyrics_upper, background="black")
        self.label_lyrics_upper.update()

        self.lyrics_lower = self.music_obj.GetLyrics(self.display_line_lower)
        self.label_lyrics_lower.configure(text = self.lyrics_lower, background="black")
        self.label_lyrics_lower.update()
        '''

        if self.display_line_upper == self.yellow_display_num:
            self.lyrics_upper = self.music_obj.GetLyrics(self.display_line_upper)
            self.label_lyrics_upper.configure(text = self.lyrics_upper, foreground="yellow",background="black")
            self.label_lyrics_upper.update()

            self.lyrics_lower = self.music_obj.GetLyrics(self.display_line_lower)
            self.label_lyrics_lower.configure(text = self.lyrics_lower, foreground="white",background="black")
            self.label_lyrics_lower.update()
        else:
            self.lyrics_upper = self.music_obj.GetLyrics(self.display_line_upper)
            self.label_lyrics_upper.configure(text = self.lyrics_upper, foreground="white",background="black")
            self.label_lyrics_upper.update()

            self.lyrics_lower = self.music_obj.GetLyrics(self.display_line_lower)
            self.label_lyrics_lower.configure(text = self.lyrics_lower, foreground="yellow", background="black")
            self.label_lyrics_lower.update()



    def value_changed(self,*args):

        self.level_tempo = int(self.myval.get())

        self.label_tempo.configure(text = str(self.level_tempo), background="black")
        self.label_tempo.update()


    def NavigateScore(self):

        if self.sound_status == Sound.PLAY_STATUS:
            self.PlayBack('next')

    def TempoSound(self):

        import time

        self.navigate_thread = threading.Thread(target=self.NavigateScore)
        self.navigate_thread.start()

        proofreading_metronome = 0.0 

        while self.working_app: 
            while self.button_status:# and self.working_app:

                #start = time.time()
                beat_time = 60.0 / self.level_tempo

                if self.beat_count == 0:
                    self.high_sound.play()
                    self.navigate_thread = threading.Thread(target=self.NavigateScore)
                    self.navigate_thread.start()
                else:
                    self.low_sound.play()

                self.beat_count = self.beat_count + 1
                if self.beat_count >= int(self.beat_num.get()):
                     self.beat_count = 0

                #proofreading_metronome = time.time() - start
                time.sleep(beat_time - proofreading_metronome)
                #print(float(elapsed_time))

    def MetronomeTest(self):

        if self.sound_status == Sound.NONE_STATUS or self.sound_status == Sound.TEST_STATUS:
            if self.button_status == False:
                self.button_status = True 
                self.label_tempo.configure(foreground='#00ff00')
                self.button_style.configure('m.TButton',foreground='green')
                self.sound_status = Sound.TEST_STATUS
            else:
                self.button_status = False
                self.label_tempo.configure(foreground='#ffffff')
                self.button_style.configure('m.TButton',foreground='white')
                self.beat_count = 0
                self.sound_status = Sound.NONE_STATUS

    def PlayButton(self):

        if self.sound_status == Sound.TEST_STATUS:
            self.button_status = False
            self.working_app = False
            self.metronome_thread.join()
            self.navigate_thread.join()

            self.working_app = True 
            self.button_status = True 
            self.beat_count = 0
            self.button_style.configure('m.TButton',foreground='white')
            self.label_tempo.configure(foreground='#00ff00')
            self.button_style.configure('p.TButton',foreground='green',background='black')
            self.metronome_thread = threading.Thread(target=self.TempoSound)
            self.metronome_thread.start()

            self.sound_status = Sound.PLAY_STATUS

            print('PlayButton')

        elif self.sound_status == Sound.NONE_STATUS:
            self.button_status = True 
            self.label_tempo.configure(foreground='#00ff00')
            #self.beat_count = 0
            self.button_style.configure('p.TButton',foreground='green',background='black')
            self.sound_status = Sound.PLAY_STATUS
            
        else: #Sound.PLAY_STATUS
            self.button_status = False
            self.label_tempo.configure(foreground='#ffffff')
            self.button_style.configure('p.TButton',foreground='white',background='black')
            self.sound_status = Sound.NONE_STATUS
            self.beat_count = 0



    def VolumeButton(self):

        if self.volume_on == False:
            self.high_sound.set_volume(1)
            self.low_sound.set_volume(1)
            self.volume_on = True 
            self.volume_style.configure('v.TButton',foreground='green',background='black')
        else:
            self.high_sound.set_volume(0)
            self.low_sound.set_volume(0)
            self.volume_on = False
            self.volume_style.configure('v.TButton',foreground='white',background='black')


    def TransposeProcess(self,trans_code):
        self.music_obj.TransposeScale(trans_code)

        self.chord_upper = self.music_obj.GetChord(self.display_line_upper)
        self.chord_upper = self.music_obj.TransposeChord(self.chord_upper)

        self.label_chord_upper.configure(text = self.chord_upper, background="black")
        self.label_chord_upper.update()

        self.chord_lower = self.music_obj.GetChord(self.display_line_lower)
        self.chord_lower = self.music_obj.TransposeChord(self.chord_lower)
        self.label_chord_lower.configure(text = self.chord_lower, background="black")
        self.label_chord_lower.update()


    def PlayBack(self, playback_code):

        if playback_code == 'back':
            if self.playback_status == Playback.END_POSITION:
                self.playback_status = Playback.MIDWAY_POSITION
                self.yellow_display_num = self.yellow_display_num - 1
                print(self.yellow_display_num)
                print(self.lyrics_num)
            elif self.lyrics_num[0] != 0:
                self.lyrics_num[1] = self.lyrics_num[0]
                self.lyrics_num[0] = self.lyrics_num[0] - 1 
                self.yellow_display_num = self.yellow_display_num - 1
                self.playback_status = Playback.MIDWAY_POSITION
                print(self.yellow_display_num)
                print(self.lyrics_num)
            elif self.lyrics_num[0] == 0 and self.playback_status != Playback.START_POSITION:
                #self.yellow_display_num = self.yellow_display_num - 1
                self.playback_status = Playback.START_POSITION
                print(self.yellow_display_num)
                print(self.lyrics_num)
            else:
                return
        elif playback_code == 'next':
            if self.lyrics_num[1] != self.music_obj.GetLyricsEndnum():
                self.lyrics_num[0] = self.lyrics_num[1]
                self.lyrics_num[1] = self.lyrics_num[1] + 1
                self.yellow_display_num = self.yellow_display_num + 1
                self.playback_status = Playback.MIDWAY_POSITION
                print(self.yellow_display_num)
                print(self.lyrics_num)
            elif self.lyrics_num[1] == self.music_obj.GetLyricsEndnum() and self.playback_status != Playback.END_POSITION:
                self.yellow_display_num = self.yellow_display_num + 1
                self.playback_status = Playback.END_POSITION
                print(self.yellow_display_num)
                print(self.lyrics_num)
            else:
                return
        else:
            return


        if self.lyrics_num[0] % 2 == 0:
            self.display_line_upper = self.lyrics_num[0]
            self.display_line_lower = self.lyrics_num[1]
        else:
            self.display_line_upper = self.lyrics_num[1]
            self.display_line_lower = self.lyrics_num[0]

        #print(self.display_line_upper)
        #print(self.display_line_lower)

        self.DisplayChord()
        self.DisplayLyrics()


        #print(self.lyrics_num)



        
    def QuitApp(self):

        self.button_status = False
        self.volume_on = False
        self.working_app = False

        self.metronome_thread.join()
        self.navigate_thread.join()
        self.master.destroy()


    def CreateListbox(self):
        #artist_list = os.listdir(self.music_obj.MUSIC_DIR)

        
        #Artist_Listbox
        self.lb_artist = Listbox(self.main_frame, listvariable = StringVar(value=self.artist_list), height = 7, background = "black",foreground = "white")
        self.lb_artist.bind(
                    "<<ListboxSelect>>",
                    self.SelectArtist,
                )
        self.lb_artist.grid(row=0, column=0, rowspan = 2, padx = 5, pady = 5,sticky=(N,E,W,S))
        

        # Artist_Scrollbar
        self.artist_scrollbar = ttk.Scrollbar(
            self.main_frame, 
            orient=VERTICAL, 
            command=self.lb_artist.yview,
            )

        self.lb_artist['yscrollcommand'] = self.artist_scrollbar.set
        self.artist_scrollbar.grid(row = 0,column = 1, rowspan = 2, padx = 5, pady = 5,sticky=(N,S))

        #Music_Listbox
        self.lb_music = Listbox(self.main_frame, listvariable = StringVar(value=self.music_list), height = 7, background = "black",foreground = "white")
        '''
        self.lb_music.bind(
                    "<<ListboxSelect>>",
                    self.Template,
                )
                '''
        self.lb_music.grid(row=2, column=0, rowspan = 3, padx = 5, pady = 5,sticky=(N,E,W,S))

        # Music_Scrollbar
        self.music_scrollbar = ttk.Scrollbar(
            self.main_frame, 
            orient=VERTICAL, 
            command=self.lb_music.yview,
            )
        

        self.lb_music['yscrollcommand'] = self.music_scrollbar.set
        self.music_scrollbar.grid(row = 2,column = 1, rowspan = 3 ,padx = 5, pady = 5,sticky=(N,S))


    def CreateMetronome(self):

        #Metronome test Button
        self.button_style = ttk.Style()
        self.button_style.configure('m.TButton',foreground='white',background='black')
        self.metronome_test_button = ttk.Button(self.main_frame, text = 'metronome_test',width = 20 ,command = self.MetronomeTest,style='m.TButton')
        self.metronome_test_button.grid(row = 4, column = 6, padx = 5, pady = 5,sticky = (N, E, W, S))

        #Tempo scale 
        self.myval = DoubleVar()
        self.myval.trace("w", self.value_changed)

        sc = ttk.Scale(
                self.main_frame,
                variable = self.myval,
                orient = HORIZONTAL,
                length = 200,
                from_ = 40,
                to = 208)
        sc.grid(row = 1, column = 6, sticky = (E,W))

        #Volume Button 
        self.volume_style = ttk.Style()
        self.volume_style.configure('v.TButton',foreground='green',background='black')
        self.volume_button = ttk.Button(self.main_frame, text = 'Volume' ,width = 20, command = self.VolumeButton,style='v.TButton')
        self.volume_button.grid(row = 2, column = 6, padx = 5, pady = 5,sticky = (N, E, W, S))

        #Combobox
        self.beat_num = StringVar()
        cb = ttk.Combobox(
                self.main_frame,
                textvariable = self.beat_num,
                value = self.beat_list,
                width = 10)
        cb.set(self.beat_list[2])
        cb.grid(row = 3, column = 6, padx = 5, pady = 5)

        #Tempo level label
        self.label_tempo = ttk.Label(self.main_frame, text = str(self.level_tempo), font = ("",35), background = "black", foreground = "white")
        self.label_tempo.grid(row = 0, column = 6, padx = 5, pady = 5,sticky = S)

        self.metronome_thread = threading.Thread(target=self.TempoSound)
        self.metronome_thread.start()


    def CreateWidget(self):

        self.CreateListbox()

        #Music_Button
        button_style = ttk.Style()
        button_style.configure('s.TButton',foreground='white',background='black')
        self.music_button = ttk.Button(self.main_frame, text = 'OK', command = self.SelectMusic,style='s.TButton')
        self.music_button.grid(row = 5, column = 0, sticky = (N, E, W, S))


        #lyrics and chord display (label)
        self.label_lyrics_upper = ttk.Label(self.main_frame, text = self.lyrics_upper, font = ("",40), background = "black", foreground = "yellow")
        self.label_lyrics_upper.grid(row = 6, column = 0, columnspan = 7, sticky = W)

        self.label_chord_upper = ttk.Label(self.main_frame, text = self.chord_upper, font = ("",40), background = "black", foreground = "yellow")
        self.label_chord_upper.grid(row = 7, column = 0, columnspan = 7, sticky = W)
        
        self.label_lyrics_lower = ttk.Label(self.main_frame, text = self.lyrics_lower, font = ("",40), background = "black", foreground = "white")
        self.label_lyrics_lower.grid(row = 8, column = 0, columnspan = 7, sticky = W)

        self.label_chord_lower = ttk.Label(self.main_frame, text = self.chord_lower, font = ("",40), background = "black", foreground = "white")
        self.label_chord_lower.grid(row = 9, column = 0, columnspan = 7, sticky = W)


        #music and artist display (label)
        self.label_music = ttk.Label(self.main_frame, text = self.music_name, font = ("",40), background = "black", foreground = "white")
        self.label_music.grid(row = 0, column = 2, columnspan = 4)

        self.label_artist = ttk.Label(self.main_frame, text = self.artist_name.replace('/',''), font = ("",30), background = "black", foreground = "white")
        self.label_artist.grid(row = 1, column = 2, columnspan = 4)

        #play_Button
        self.button_style = ttk.Style()
        self.button_style.configure('p.TButton',foreground='white',background='black')
        self.music_button = ttk.Button(self.main_frame, text = 'Play', command = self.PlayButton,style='p.TButton')
        self.music_button.grid(row = 2, column = 3, columnspan = 2,padx = 5, pady = 5, sticky = (N, E, W, S))

        #Combobox
        self.interval_num = StringVar()
        cb = ttk.Combobox(
                self.main_frame,
                textvariable = self.interval_num,
                value = self.INTERVAL_LIST,
                width = 10)
        cb.set(self.INTERVAL_LIST[2])
        cb.grid(row = 3, column = 3, columnspan = 2)

        #play_display
        self.label_play_display = ttk.Label(self.main_frame, text = 'play_display_test',font = ("",20), background = "black", foreground = "white")
        self.label_play_display.grid(row = 4, column = 3, columnspan=2)


        #playback_location(left)_button
        button_style = ttk.Style()
        button_style.configure('pll.TButton',foreground='white',background='black')
        self.playback_left_button = ttk.Button(self.main_frame, text = '◀', command = lambda:self.PlayBack('back'),style='pll.TButton')
        self.playback_left_button.grid(row = 2, column = 2, padx = 5, pady = 5, sticky = (N,E,W,S))

        #playback_location(right)_button
        button_style = ttk.Style()
        button_style.configure('plr.TButton',foreground='white',background='black')
        self.playback_right_button = ttk.Button(self.main_frame, text = '▶', command = lambda:self.PlayBack('next'),style='plr.TButton')
        self.playback_right_button.grid(row = 2, column = 5, padx = 5, pady = 5, sticky = (N,E,W,S))


        #Transposition_plus_button
        button_style = ttk.Style()
        button_style.configure('tp.TButton',foreground='white',background='black')
        self.transposition_plus_button = ttk.Button(self.main_frame, text = '+', command = lambda:self.TransposeProcess('plus'),style='tp.TButton')
        self.transposition_plus_button.grid(row = 5, column = 4, padx = 5, pady = 5, sticky = (N,E,W,S))

        #Transposition_minus_button
        button_style = ttk.Style()
        button_style.configure('tm.TButton',foreground='white',background='black')
        self.transposition_minus_button = ttk.Button(self.main_frame, text = '-', command = lambda:self.TransposeProcess('minus'),style='tm.TButton')
        self.transposition_minus_button.grid(row = 5, column = 3, padx = 5, pady = 5, sticky = (N,E,W,S))


        self.CreateMetronome()

        self.master.protocol("WM_DELETE_WINDOW",self.QuitApp)

        self.master.mainloop()




if __name__ == '__main__':

    tkinter_obj = Tk()

    main_obj = MainWindow(tkinter_obj)

    main_obj.CreateWidget()

