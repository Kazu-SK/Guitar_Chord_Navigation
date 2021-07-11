
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from tkinter.font import Font

from pathlib import Path

import os
import sys 
import glob


class MainWindow(ttk.Frame):

    def __init__(self,master = None):
        self.Config()

        master.title('lyrics_and_chord')
        master["bg"] = "black"

        frame_style = ttk.Style()
        frame_style.configure('s.TFrame',background='black')
        self.main_frame = super().__init__(master,style='s.TFrame')

        self.grid()

        print('init')

        master.grid_columnconfigure(0,weight=1)
        master.grid_columnconfigure(1,weight=1)

        master.grid_rowconfigure(3,weight=1)


    def Config(self):
        print('config')
        self.MUSIC_DIR = os.path.abspath("music/")


    def SaveButton(self):

        artist_list = []
        artist_name = self.text_artist.get('1.0','end-1c') 
        musit_name = self.text_music.get('1.0', 'end-1c')

        file_list = os.listdir(self.MUSIC_DIR)

        for f in file_list:
            if os.path.isfile(os.path.join(self.MUSIC_DIR,f)) == False:
                artist_list.append(f)

        if artist_name not in artist_list:
            os.mkdir(self.MUSIC_DIR + '/' + artist_name)

        print(artist_list)


    def ReadButton(self):
        print('read')


    def CreateWidget(self):
        print('createwidget')
        

        ''' Label '''
        #artist label
        self.label_artist = ttk.Label(self.main_frame, text = 'Artist', font = ("",35), background = "black", foreground = "white")
        self.label_artist.grid(row = 0, column = 0, columnspan = 2)

        #music name label
        self.label_music_name = ttk.Label(self.main_frame, text = 'Music name', font = ("",35), background = "black", foreground = "white")
        self.label_music_name.grid(row = 2, column = 0, columnspan = 2)

        #lyrics label
        self.label_lyrics = ttk.Label(self.main_frame, text = 'Lyrics', font = ("",35), background = "black", foreground = "white")
        self.label_lyrics.grid(row = 4, column = 0)

        #guitar chord label
        self.label_lyrics = ttk.Label(self.main_frame, text = 'Chord', font = ("",35), background = "black", foreground = "white")
        self.label_lyrics.grid(row = 4, column = 1)


        ''' Text '''
        f = Font(family='Helvetica', size=16)
        #artist text
        self.text_artist = Text(self.main_frame, height=1, width=30)
        self.text_artist.configure(font=f)
        self.text_artist.grid(row=1, column=0, columnspan = 2,padx = 10, pady = 10)

        #music text
        self.text_music = Text(self.main_frame, height=1, width=30)
        self.text_music.configure(font=f)
        self.text_music.grid(row=3, column=0, columnspan = 2,padx = 10, pady = 10)

        #lyrics text
        self.text_lyrics = Text(self.main_frame, height=15, width=70)
        self.text_lyrics.configure(font=f)
        self.text_lyrics.grid(row=5, column=0, padx = 10, pady = 10, sticky=(N, W, S, E))

        #text_chord
        self.text_chord = Text(self.main_frame, height=15, width=70)
        self.text_chord.configure(font=f)
        self.text_chord.grid(row=5, column=1, padx = 10, pady = 10, sticky=(N, W, S, E))

        ''' Button '''
        #save_button
        button_style = ttk.Style()
        button_style.configure('ok.TButton',foreground='white',background='black')
        self.volume_button = ttk.Button(self.main_frame, text = 'SAVE' ,width = 20, command = self.SaveButton,style='ok.TButton')
        self.volume_button.grid(row = 6, column = 1, padx = 5, pady = 5, sticky = W)

        #read_button
        button_style.configure('read.TButton',foreground='white',background='black')
        self.volume_button = ttk.Button(self.main_frame, text = 'READ' ,width = 20, command = self.ReadButton,style='read.TButton')
        self.volume_button.grid(row = 6, column = 0, padx = 5, pady = 5, sticky = E)

        self.master.mainloop()
        


if __name__ == '__main__':

    tkinter_obj = Tk()

    main_obj = MainWindow(tkinter_obj)

    main_obj.CreateWidget()

