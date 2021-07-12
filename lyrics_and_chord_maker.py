
from tkinter import *
from tkinter import ttk
import tkinter as tk 
from tkinter import filedialog

from tkinter.font import Font

from pathlib import Path

import os
import sys 
import glob


'''
class ErrorWindow(ttk.Frame):

    def __init__(self,master = None):
        master.title('Error')
        master["bg"] = "black"

        frame_style = ttk.Style()
        frame_style.configure('error.TFrame',background='black')
        self.error_frame = super().__init__(master,style='error.TFrame')

        self.grid()

    def CreateWidget(self):
        self.label_error = ttk.Label(self.error_frame, text = 'Error', font = ("",35), background = "black", foreground = "white")
        self.label_error.grid(row = 0, column = 0, padx = 10, pady = 10, sticky=(N,E,W,S))

        self.master.mainloop()
'''


class MainWindow(ttk.Frame):

    def __init__(self,master = None):
        self.Config()

        master.title('lyrics_and_chord')
        master["bg"] = "black"

        frame_style = ttk.Style()
        frame_style.configure('s.TFrame',background='black')
        self.main_frame = super().__init__(master,style='s.TFrame')

        self.grid()


        master.grid_columnconfigure(0,weight=1)
        master.grid_columnconfigure(1,weight=1)

        master.grid_rowconfigure(5,weight=1)


    def Config(self):
        self.MUSIC_DIR = os.path.abspath("music/")
        self.SPACE_CHORD = '            /            '

        self.DETAIL_ERROR = 'Please fill in the blank.'


    def Error(self,a_name, m_name,l_str,c_str):

        def error_window():
            error_win = tk.Toplevel()
            error_win.geometry("300x100")

            label_error = tk.Label(error_win, text="Error", font = ("",30), foreground = "red")
            label_error.pack()
            label_detail = tk.Label(error_win, text=self.DETAIL_ERROR, font = ("",20))
            label_detail.pack()


        if a_name == '' or m_name == '' or l_str == '' or c_str == '':
            error_window()

            return True 

        return False


    def SaveButton(self):

        artist_list = []
        artist_name = self.text_artist.get('1.0','end-1c') 
        music_name = self.text_music.get('1.0', 'end-1c')
        lyrics_str = self.text_lyrics.get('1.0', 'end-1c')
        chord_str = self.text_chord.get('1.0', 'end-1c')


        if self.Error(artist_name, music_name, lyrics_str, chord_str) == True:
            return

        file_list = os.listdir(self.MUSIC_DIR)

        for f in file_list:
            if os.path.isfile(os.path.join(self.MUSIC_DIR,f)) == False:
                artist_list.append(f)

        if artist_name not in artist_list:
            os.mkdir(self.MUSIC_DIR + '/' + artist_name)

        save_dir = self.MUSIC_DIR + '/' + artist_name + '/'

        table = lyrics_str.maketrans({'\u3000':' '})
        lyrics_str = lyrics_str.translate(table)

        table = chord_str.maketrans({'\u3000':' '})
        chord_str = chord_str.translate(table)

        lyrics_output = lyrics_str.split('\n')
        chord_output = chord_str.split('\n')

        lyrics_list = []
        chord_list = []
        music_list = []

        for lyrics_lines ,lyrics in enumerate(lyrics_output):
            lyrics_list.append('lyrics:'+lyrics+'\n')

        for chord_lines ,chord in enumerate(chord_output):
            chord_list.append('chord_:'+chord+'\n')


        if lyrics_lines > chord_lines:
            for i in range(lyrics_lines-chord_lines):
                chord_list.append('chord_:'+self.SPACE_CHORD+'\n')
        elif chord_lines > lyrics_lines:
            for i in range(chord_lines-lyrics_lines):
                lyrics_list.append('lyrics:'+self.SPACE_CHORD+'\n')
        else:
            pass


        file_list = os.listdir(self.MUSIC_DIR+'/'+artist_name+'/')

        for f in file_list:
            if os.path.isfile(os.path.join(self.MUSIC_DIR+'/'+artist_name+'/',f)) == True:
                music_list.append(f)


        file_name = music_name + '.txt'

        if file_name in music_list:
            file_obj = open(save_dir+file_name,'w') #over write
        else:
            file_obj = open(save_dir+file_name,'x') #new

        file_obj.writelines(lyrics_list)
        file_obj.writelines(chord_list)
                        
        file_obj.close()


    def LoadButton(self):
        print('load')


    def CreateWidget(self):

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
        self.volume_button = ttk.Button(self.main_frame, text = 'LOAD' ,width = 20, command = self.LoadButton,style='read.TButton')
        self.volume_button.grid(row = 6, column = 0, padx = 5, pady = 5, sticky = E)

        self.master.mainloop()
        


if __name__ == '__main__':

    tkinter_obj = Tk()

    main_obj = MainWindow(tkinter_obj)

    main_obj.CreateWidget()

