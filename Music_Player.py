#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 19:52:11 2022

@author: Mai
"""

from wav_to_sheet import WavToSheet
from tkinter import *
from pygame import mixer
from tkinter import Label
from tkinter import Button
from tkinter import filedialog
from PIL import ImageTk, Image
from pdf2image import convert_from_path
import os
import librosa
#import time

os.chdir('/Users/Mai/Documents/ME396P/Final Project')
#setting colors
col1 = "#ffffff"
col2 = "#333333"
col3 = '#7F7FFF'


window = Tk()
window.title("Music Player")
window.geometry('1500x450')
window.configure(background = col2)
window.resizable(width = FALSE, height = FALSE)


#Frames

top_frame = Frame(window, width = 1496, height = 200, bg = col1)
top_frame.grid(row =0, column = 0, columnspan = 1, padx =2, pady=2)
middle_frame = Frame(window, width = 1496, height = 100, bg = col2)
middle_frame.grid(row =2, column = 0, columnspan = 1,padx =1, pady=1)
bottom_frame = Frame(window, width = 1496, height = 100, bg = col2)
bottom_frame.grid(row =3, column = 0, columnspan = 1,padx =1, pady=1)
bottom_frame_text = Frame(window, width = 1496, height = 50, bg = col1)
bottom_frame_text.grid(row =4, column = 0, columnspan = 1,padx =2, pady=2)


#Functions
def upload():  
    '''
    Converts audio to sheet music & crops sheet music to separate images
    '''
    global music_file, audio_length
    running_song['text'] = 'Loading'
    
    
    music_file = filedialog.askopenfilename()
    WavToSheet(music_file)
    
    
    Sheet_music = music_file.split('/')[-1]
    Sheet_music = Sheet_music.split('.wav')[0]+'SheetMusic.pdf' 
    pages = convert_from_path(Sheet_music, 300)
    for page in pages:
        page.save(Sheet_music.split('.pdf')[0]+'.png', 'PNG')
    Sheet_img = Image.open(Sheet_music.split('.pdf')[0]+'.png')
    width, height = Sheet_img.size
    #print(width,height)
    #Setting the points for cropped image
    left = 50
    top = 137
    right = (width)-50
    bottom = height/2

    im1 = Sheet_img.crop((left, top, right, bottom)) #Cropped image of above dimension
    
    width, height = im1.size
    for i in range(6):
        left2 = 0
        top2 = (height/7)*i
        right2 = right
        bottom2 = (height/7)*(i+1)
        im2 = im1.crop((left2, top2, right2, bottom2))
        im2 = im2.resize((496*3,200))
        im2.save('crop_' + str(i)+'.png')
        
    running_song['text'] = 'Loaded'
    audio_length = librosa.get_duration(filename=music_file.split('/')[-1])
    return music_file, audio_length
        

def play(music_file): 
    '''Plays audio file 
    '''
    global playing_state,i
    i = 0
    print(music_file)
    #music_file = filedialog.askopenfilename()  
    mixer.init()
    mixer.music.load(music_file)
    mixer.music.play()
    playing_state = True

    running_song['text'] = music_file.split('/')[-1]
    return i
    #print(music_file)
    
    
def display():
    '''Displays changing sheet music along with audio
    '''
    global i, playing_state, audio_length
    no_of_bars = 3
    if playing_state:
        while i < no_of_bars:
        
            im3 = ImageTk.PhotoImage(Image.open('crop_' + str(i)+'.png'),master=window)
            Sheet_frame.image = im3
            Sheet_frame.configure(image = im3)

            i+=1

            break

        Sheet_frame.after(int((audio_length/no_of_bars)*1000),display)
    else:
        return
        
def pause():
    '''Pauses audio file 
    '''
    global playing_state
    mixer.music.pause()
    playing_state = False 

def resume():
    '''Resumes audio file 
    '''
    global playing_state
    mixer.music.unpause()
    playing_state = True
    
#initializing variables
music_file = ''
playing_state = False
i = 0
audio_length = 0

#Buttons
Upload_img = Image.open('Icons/upload.png') 
Upload_img = Upload_img.resize((50,50))
Upload_img = ImageTk.PhotoImage(Upload_img,master=window)
Upload_button = Button(bottom_frame, height = 50, image = Upload_img,bg = col1,command=upload)
Upload_button.place(x = 1500/8, y = 50, anchor ='center')

Play_img = Image.open('Icons/play.png') 
Play_img = Play_img.resize((50,50))
Play_img = ImageTk.PhotoImage(Play_img,master=window)
Play_button = Button(bottom_frame, height = 50, image = Play_img,bg = col1, command=lambda:[play(music_file), display()])
Play_button.place(x = (1500/8)*3, y = 50, anchor ='center')

Pause_img = Image.open('Icons/pause.png') 
Pause_img = Pause_img.resize((50,50))
Pause_img = ImageTk.PhotoImage(Pause_img,master=window)
Pause_button = Button(bottom_frame, height = 50, image = Pause_img, bg = col1, command=lambda:[pause(), display()])
Pause_button.place(x = (1500/8)*5, y = 50, anchor ='center')

Resume_img = Image.open('Icons/resume.png') 
Resume_img = Resume_img.resize((50,50))
Resume_img = ImageTk.PhotoImage(Resume_img,master=window)
Resume_button = Button(bottom_frame, height = 50, image = Resume_img,bg = col1, command=lambda:[resume(), display()])
Resume_button.place(x = (1500/8)*7, y = 50, anchor ='center')

Sheet_frame = Label(top_frame, height = 200)
Sheet_frame.place(x = 1500/2, y = 100, anchor ='center') 

Play_to_external_device = Button(middle_frame, text = ('Play to External Device'), font=("Arial",30),fg = 'black')
Play_to_external_device.place(x = 1500/2, y = 50, anchor ='center')

running_song = Label(bottom_frame_text,text ='Load',font=("Arial",25) ,fg = 'black')
running_song.place(x = (1500/2), y = 20, anchor ='center')


        


window.mainloop()