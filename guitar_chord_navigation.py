

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

        self.Config()

        master.title('Guitar_chord and lyrics Navigation')
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


        self.yellow_display_num = 0



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

        self.proofreading_file = open("proofreading.txt","+r")
        self.proofreading_metronome = float(self.proofreading_file.read()) 
        #self.proofreading_file.truncate(0)
        self.proofreading_file.close()

        print(self.proofreading_metronome)


        #lyrics and chord scroll
        self.lyrics_num = [0, 1]
        self.loop_count = 0
        self.scroll_flag = False


        #column row configure
        for i in range(2,8):
            master.grid_columnconfigure(i,weight=1)

        master.grid_columnconfigure(0,weight=1)

        for j in range(10):
            master.grid_rowconfigure(j,weight=1)
    

    def Config(self):
        self.INTERVAL_LIST = [1,2,3,4]

        self.LABEL_INTERVAL_BAR = 'Interval(bar)'
        self.LABEL_BEAT = 'Beat'

        self.LABEL_PLAY = 'Play'
        self.LABEL_INTERVAL = 'Intereval'
        self.LABEL_STOP = 'Stop'
        self.LABEL_END = 'End'



    def SelectArtist(self,event):

        for i in self.lb_artist.curselection():
            self.artist_name = self.lb_artist.get(i)

        self.music_list = self.music_obj.MusicList(self.artist_name)

        self.lb_music.configure(listvariable = StringVar(value=self.music_list)) 
        self.lb_music.update()


    def SelectMusic(self):

        for i in self.lb_music.curselection():
            self.music_name = self.lb_music.get(i)

        
        if self.music_obj.GetMusicinfo(self.artist_name,self.music_name) != True:
            return 

        self.display_line_upper = 0
        self.display_line_lower = 1

        self.music_obj.InitializeScale()
        self.label_scale_num.configure(text = self.music_obj.GetScalenum())
        self.label_scale_num.update()


        self.label_music.configure(text = self.music_name, foreground="white",background="black")
        self.label_artist.configure(text = self.artist_name.replace('/',''), foreground="white",background="black")
        self.label_music.update()
        self.label_artist.update()


        self.lyrics_num = [0, 1]
        self.yellow_display_num = 0

        self.DisplayChord()
        self.DisplayLyrics()


    def DisplayChord(self):

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


        self.loop_count = self.loop_count + 1

        if self.sound_status == Sound.PLAY_STATUS and self.scroll_flag == True and self.loop_count >= 2:
            self.PlayBack('next')
            self.loop_count = 0
        else:
            if self.scroll_flag == True:
                return
            else:
                self.label_play_display.configure(text = self.LABEL_INTERVAL,foreground="yellow", background="black")

            if self.loop_count > int(self.interval_num.get()):
                if  self.sound_status == Sound.PLAY_STATUS: 
                    self.scroll_flag = True
                    self.label_play_display.configure(text = self.LABEL_PLAY,foreground="green", background="black")
                
                self.loop_count = 0


    def PFminus(self):
        self.proofreading_metronome = self.proofreading_metronome - 5 


    def PFplus(self):
        self.proofreading_metronome = self.proofreading_metronome + 5 


    def TempoSound(self):

        import time

        def AbandonedStone(): 
            return

        self.navigate_thread = threading.Thread(target=AbandonedStone)
        self.navigate_thread.start()


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

                time.sleep(beat_time + self.proofreading_metronome/1000.0)
                #wait_timer = time.time() - start
                #print(float(wait_timer))

    def MetronomeTest(self):

        if self.sound_status == Sound.NONE_STATUS or self.sound_status == Sound.TEST_STATUS:
            if self.button_status == False:
                self.button_status = True 
                self.label_tempo.configure(foreground='#00ff00')
                self.metronome_button_style.configure('m.TButton',foreground='green')
                self.sound_status = Sound.TEST_STATUS
            else:
                self.button_status = False
                self.label_tempo.configure(foreground='#ffffff')
                self.metronome_button_style.configure('m.TButton',foreground='white')
                self.beat_count = 0

                #scroll
                self.loop_count = 0
                self.label_play_display.configure(text = self.LABEL_STOP,foreground="red", background="black")

                self.sound_status = Sound.NONE_STATUS

    def PlayButton(self):

        if self.sound_status == Sound.TEST_STATUS:
            self.button_status = False
            self.working_app = False
            self.beat_count = 0
            self.metronome_thread.join()
            self.navigate_thread.join()

            #initialize for play
            self.working_app = True 
            self.button_status = True 
            self.loop_count = 0
            self.scroll_flag = False

            self.metronome_button_style.configure('m.TButton',foreground='white')
            self.label_tempo.configure(foreground='#00ff00')
            self.play_button_style.configure('p.TButton',foreground='green',background='black')
            self.metronome_thread = threading.Thread(target=self.TempoSound)
            self.metronome_thread.start()

            self.sound_status = Sound.PLAY_STATUS


        elif self.sound_status == Sound.NONE_STATUS:
            self.button_status = True 
            self.label_tempo.configure(foreground='#00ff00')
            self.play_button_style.configure('p.TButton',foreground='green',background='black')
            self.scroll_flag = False
            self.sound_status = Sound.PLAY_STATUS
            
        else: #Sound.PLAY_STATUS
            self.button_status = False
            self.label_tempo.configure(foreground='#ffffff')
            self.play_button_style.configure('p.TButton',foreground='white',background='black')
            self.sound_status = Sound.NONE_STATUS
            self.beat_count = 0
            self.loop_count = 0
            self.scroll_flag = False
            self.label_play_display.configure(text = self.LABEL_STOP,foreground="red", background="black")



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

        self.label_scale_num.configure(text = self.music_obj.GetScalenum())
        self.label_scale_num.update()


    def PlayBack(self, playback_code):

        if playback_code == 'back':
            if self.playback_status == Playback.END_POSITION:
                self.playback_status = Playback.MIDWAY_POSITION
                self.yellow_display_num = self.yellow_display_num - 1
            elif self.lyrics_num[0] != 0:
                self.lyrics_num[1] = self.lyrics_num[0]
                self.lyrics_num[0] = self.lyrics_num[0] - 1 
                self.yellow_display_num = self.yellow_display_num - 1
                self.playback_status = Playback.MIDWAY_POSITION
            elif self.lyrics_num[0] == 0 and self.playback_status != Playback.START_POSITION:
                self.playback_status = Playback.START_POSITION
            else:
                return
        elif playback_code == 'next':
            if self.lyrics_num[1] != self.music_obj.GetLyricsEndnum():
                self.lyrics_num[0] = self.lyrics_num[1]
                self.lyrics_num[1] = self.lyrics_num[1] + 1
                self.yellow_display_num = self.yellow_display_num + 1
                self.playback_status = Playback.MIDWAY_POSITION
            elif self.lyrics_num[1] == self.music_obj.GetLyricsEndnum() and self.playback_status != Playback.END_POSITION:
                self.yellow_display_num = self.yellow_display_num + 1
                self.playback_status = Playback.END_POSITION
            else:
                #End
                if self.sound_status == Sound.PLAY_STATUS:
                    self.label_play_display.configure(text = self.LABEL_END,foreground='skyblue', background="black")

                return
        else:
            return


        if self.lyrics_num[0] % 2 == 0:
            self.display_line_upper = self.lyrics_num[0]
            self.display_line_lower = self.lyrics_num[1]
        else:
            self.display_line_upper = self.lyrics_num[1]
            self.display_line_lower = self.lyrics_num[0]


        self.DisplayChord()
        self.DisplayLyrics()


        
    def QuitApp(self):

        self.button_status = False
        self.volume_on = False
        self.working_app = False

        self.proofreading_file = open("proofreading.txt","w")

        #self.proofreading_file.truncate(0)
        self.proofreading_file.write(str(self.proofreading_metronome))
        self.proofreading_file.close()

        self.metronome_thread.join()
        self.navigate_thread.join()
        self.master.destroy()


    def CreateListbox(self):
        
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
        music_scrollbar = ttk.Scrollbar(
            self.main_frame, 
            orient=VERTICAL, 
            command=self.lb_music.yview,
            )
        

        self.lb_music['yscrollcommand'] = music_scrollbar.set
        music_scrollbar.grid(row = 2,column = 1, rowspan = 3 ,padx = 5, pady = 5,sticky=(N,S))


    def CreateMetronome(self):

        #Metronome test Button
        self.metronome_button_style = ttk.Style()
        self.metronome_button_style.configure('m.TButton',foreground='white',background='black')
        metronome_test_button = ttk.Button(self.main_frame, text = 'metronome_test',width = 20 ,command = self.MetronomeTest,style='m.TButton')
        metronome_test_button.grid(row = 4, column = 8, columnspan = 2,padx = 5, pady = 5,sticky = (N, E, W, S))

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
        sc.grid(row = 1, column = 8, columnspan = 2, sticky = (E,W))

        #Volume Button 
        self.volume_style = ttk.Style()
        self.volume_style.configure('v.TButton',foreground='green',background='black')
        volume_button = ttk.Button(self.main_frame, text = 'Volume' ,width = 20, command = self.VolumeButton,style='v.TButton')
        volume_button.grid(row = 2, column = 8, columnspan = 2, padx = 5, pady = 5,sticky = (N, E, W, S))

        #Combobox
        label_beat = ttk.Label(self.main_frame, text = self.LABEL_BEAT, font = ("",12), background = "black", foreground = "white")
        label_beat.grid(row = 3, column = 8, padx = 5, pady = 5, sticky = E)

        self.beat_num = StringVar()
        cb = ttk.Combobox(
                self.main_frame,
                textvariable = self.beat_num,
                value = self.beat_list,
                width = 10)
        cb.set(self.beat_list[2])
        cb.grid(row = 3, column = 9, padx = 5, pady = 5, sticky = W)


        #Tempo level label
        self.label_tempo = ttk.Label(self.main_frame, text = str(self.level_tempo), font = ("",35), background = "black", foreground = "white")
        self.label_tempo.grid(row = 0, column = 8, columnspan = 2,padx = 5, pady = 5,sticky = S)

        self.metronome_thread = threading.Thread(target=self.TempoSound)
        self.metronome_thread.start()

        #Proofreading button
        proofreading_button_style = ttk.Style()

        proofreading_button_style.configure('pf_m.TButton',foreground='white',background='black')
        proofreading_minus_button = ttk.Button(self.main_frame, text = 'PR -' , command = self.PFminus,width = 20,style='pf_m.TButton')
        proofreading_minus_button.grid(row = 5, column = 8, padx = 5, pady = 5, sticky =(N,E,W,S))

        proofreading_button_style.configure('pf_p.TButton',foreground='white',background='black')
        proofreading_plus_button = ttk.Button(self.main_frame, text = 'PR +' , command = self.PFplus,width = 20,style='pf_p.TButton')
        proofreading_plus_button.grid(row = 5, column = 9, padx = 5, pady = 5, sticky = (N,E,W,S))


    def CreateWidget(self):

        self.CreateListbox()
        button_style = ttk.Style()

        #Music_Button
        button_style.configure('s.TButton',foreground='white',background='black')
        music_button = ttk.Button(self.main_frame, text = 'OK', command = self.SelectMusic,style='s.TButton')
        music_button.grid(row = 5, column = 0, sticky = (N, E, W, S))


        #lyrics and chord display (label)
        self.label_lyrics_upper = ttk.Label(self.main_frame, text = self.lyrics_upper, font = ("",40), background = "black", foreground = "yellow")
        self.label_lyrics_upper.grid(row = 6, column = 0, columnspan = 8, sticky = W)

        self.label_chord_upper = ttk.Label(self.main_frame, text = self.chord_upper, font = ("",40), background = "black", foreground = "yellow")
        self.label_chord_upper.grid(row = 7, column = 0, columnspan = 8, sticky = W)
        
        self.label_lyrics_lower = ttk.Label(self.main_frame, text = self.lyrics_lower, font = ("",40), background = "black", foreground = "white")
        self.label_lyrics_lower.grid(row = 8, column = 0, columnspan = 8, sticky = W)

        self.label_chord_lower = ttk.Label(self.main_frame, text = self.chord_lower, font = ("",40), background = "black", foreground = "white")
        self.label_chord_lower.grid(row = 9, column = 0, columnspan = 8, sticky = W)


        #music and artist display (label)
        self.label_music = ttk.Label(self.main_frame, text = self.music_name, font = ("",40), background = "black", foreground = "white")
        self.label_music.grid(row = 0, column = 2, columnspan = 6)

        self.label_artist = ttk.Label(self.main_frame, text = self.artist_name.replace('/',''), font = ("",30), background = "black", foreground = "white")
        self.label_artist.grid(row = 1, column = 2, columnspan = 6)

        #play_Button
        self.play_button_style = ttk.Style()
        self.play_button_style.configure('p.TButton',foreground='white',background='black')
        play_button = ttk.Button(self.main_frame, text = 'Play', command = self.PlayButton,style='p.TButton')
        play_button.grid(row = 2, column = 3, columnspan = 4,padx = 5, pady = 5, sticky = (N, E, W, S))

        #Interval Combobox
        self.interval_num = StringVar()
        cb = ttk.Combobox(
                self.main_frame,
                textvariable = self.interval_num,
                value = self.INTERVAL_LIST,
                width = 10)
        cb.set(self.INTERVAL_LIST[2])
        cb.grid(row = 3, column = 5, padx = 5, pady = 5,sticky = W)

        #Interval Label
        label_interval = ttk.Label(self.main_frame, text = self.LABEL_INTERVAL_BAR,font = ("",12), background = "black", foreground = "white")
        label_interval.grid(row = 3, column = 4, padx = 5, pady = 5,sticky = E)

        #play_display
        self.label_play_display = ttk.Label(self.main_frame, text = self.LABEL_STOP,font = ("",30), background = "black", foreground = "red")
        self.label_play_display.grid(row = 4, column = 3, columnspan=4)

        button_style.configure('pll.TButton',foreground='white',background='black')
        playback_left_button = ttk.Button(self.main_frame, text = '◀', command = lambda:self.PlayBack('back'),style='pll.TButton')
        playback_left_button.grid(row = 2, column = 2, padx = 5, pady = 5, sticky = (N,E,W,S))

        button_style.configure('plr.TButton',foreground='white',background='black')
        playback_right_button = ttk.Button(self.main_frame, text = '▶', command = lambda:self.PlayBack('next'),style='plr.TButton')
        playback_right_button.grid(row = 2, column = 7, padx = 5, pady = 5, sticky = (N,E,W,S))


        #Transposition_plus_button
        button_style.configure('tp.TButton',foreground='white',background='black')
        transposition_plus_button = ttk.Button(self.main_frame, text = 'key    +', command = lambda:self.TransposeProcess('plus'),style='tp.TButton')
        transposition_plus_button.grid(row = 5, column = 6, padx = 5, pady = 5, sticky = (N,E,W,S))

        #scale_num 
        self.label_scale_num = ttk.Label(self.main_frame, text = self.music_obj.GetScalenum(), font = ("",30), background = "black", foreground = "white")
        self.label_scale_num.grid(row = 5, column = 4, columnspan = 2)

        #Transposition_minus_button
        button_style.configure('tm.TButton',foreground='white',background='black')
        transposition_minus_button = ttk.Button(self.main_frame, text = 'key    -', command = lambda:self.TransposeProcess('minus'),style='tm.TButton')
        transposition_minus_button.grid(row = 5, column = 3, padx = 5, pady = 5, sticky = (N,E,W,S))


        self.CreateMetronome()

        self.master.protocol("WM_DELETE_WINDOW",self.QuitApp)

        self.master.mainloop()




if __name__ == '__main__':

    tkinter_obj = Tk()

    main_obj = MainWindow(tkinter_obj)

    main_obj.CreateWidget()

