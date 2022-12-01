#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 19:52:11 2022

@author: Mai
"""

from pathlib import Path
from wav_to_sheet.wav_to_sheet import WavToSheet
import play_external 
from play_main import *
from tkinter import *
from pygame import mixer
from tkinter import Label
from tkinter import Button
from tkinter import filedialog
from PIL import ImageTk, Image
from pdf2image import convert_from_path
import os
import librosa

os.chdir(Path.cwd())
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

#  ADD THE CLASS
class movingObj:
    def __init__(self, master=None,  x_dist=1, y_dist = 0, total_lines =3, bpm =120):
        self.master = master
        self.no_of_bars = total_lines

        self.update_delay = 49
        # x velocity of the moving bar
        self.x = x_dist
        # to take care movement in y direction
        self.y = y_dist

        self.total_steps = 81
        #self.total_steps += 2

        # canvas object to create shape
        self.canvas = Canvas(master, width = 1496, height = 200)
        # creating rectangle
        # this can choose the starting location
        self.num_moves = self.total_steps *self.no_of_bars - 1
        self.xmin = 50
        self.xmax = 60
        self.ymin = 0
        self.ymax = 200
        self.rectangle = self.canvas.create_rectangle(
                         self.xmin, self.ymin, self.xmax, self.ymax, fill = "red")

        self.canvas.pack(fill="both", expand=True)  # make sure the canvas matches the window
        #self.canvas.pack()

        #image1 = Image.open('crop_1.png')
        #im0 = ImageTk.PhotoImage(image1)  #(Image.open('crop_0.png'),master=window)
        #insert_img = im0
        #self.image_on_canvas = self.canvas.create_image(0, 0, image=insert_img, anchor="nw")
        #self.canvas.create_image(0, 0, image=im0)

        # put code here that overlays the moving object over all images

        # calling class's movement method to
        # move the rectangle
        self.counter = 0
        self.run_counter = 0
        self.extra_run = 1
        self.return_dist = self.total_steps

    def movement(self):
        global toStart
        global moving

        # This is where the move() method is called
        # This moves the rectangle to x, y coordinates

        self.canvas.tag_raise(self.rectangle)

        if self.run_counter <= self.num_moves and run == True:

            if toStart == True:
                if self.counter == 0:
                    move_shift = 0
                else:
                    move_shift = 1

                # THIS WAS TO FIX THE ISSUE WITH PLAY NOT RETURNING TO START WHEN PAUSED AT END
                if self.counter % self.total_steps == 0 and self.counter > 0:
                    move_shift = -1*(self.total_steps -1)

                # THIS WAS TO CORRECT THE ISSUE OF INCONSISTANT PLACEMENT BETWEEN FIRST LAP AND LATER LAPS
                move_back = (self.counter % self.total_steps)-move_shift
                self.canvas.move(self.rectangle, -1*self.x*(move_back), 0)
                self.counter = 0
                self.run_counter = 0
                toStart = False
                self.canvas.after(0, self.movement)

            else:

                # CHECK TO SEE IF BAR IS ON ITS LAST STEP
                # NOT ON LAST STEP
                if self.counter % self.total_steps != 0:
                    self.canvas.move(self.rectangle, self.x, self.y)
                    self.counter += 1
                    self.run_counter +=1
                    self.canvas.after(self.update_delay, self.movement)

                # FIRST STEP
                elif self.counter == 0:
                    self.counter += 1
                    self.run_counter +=1
                    self.canvas.after(0, self.movement)

                # LAST STEP
                else:

                    # IS THIS THE FIRST TIME IT'S REACHED THE LAST STEP? IF SO, MOVE ONE MORE
                    if self.counter >= self.total_steps:
                        self.canvas.move(self.rectangle, self.x, self.y)        # make loops the same each time

                    self.canvas.move(self.rectangle, -1*self.x*(self.return_dist), 0)
                    self.counter += 1
                    self.run_counter +=1
                    self.canvas.after(0, self.movement)
        else:
            moving = False


#Functions
def upload():  
    '''
    Converts audio to sheet music & crops sheet music to separate images
    '''
    global music_file, audio_length, midi_file,total_lines, bar,str_notes
    
    music_file = filedialog.askopenfilename()
    running_song['text'] = 'Loading'
    str_notes, total_lines, seconds_per_line, note_dict, bar, bpm = WavToSheet(music_file)
    
    
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
    audio_length = librosa.get_duration(filename=music_file.split('/')[-2]+'/'+music_file.split('/')[-1])
    midi_file = Sheet_music.split('.pdf')[0]+'.midi' 
    print(midi_file)
    print(total_lines)
    # insert BAR canvas object INTO FRAME
    bar = movingObj(top_frame, x_dist=18, total_lines= total_lines) 
    return music_file, audio_length, midi_file, total_lines
        

def play(music_file,rect_bar): 
    '''Plays audio file 
    '''
    global playing_state,i, moving, run, toStart
    i = 0
    print(music_file)
    #music_file = filedialog.askopenfilename()  
    mixer.init()
    mixer.music.load(music_file)
    mixer.music.play()
    playing_state = True
    
    # ADD BAR SECTION OF PLAY
    toStart = True
    run = True
    if moving == False:
        rect_bar.run_counter = 0
        rect_bar.movement()
    moving = True

    running_song['text'] = music_file.split('/')[-1]
    return i
    #print(music_file)
    
    
def display():
    '''Displays changing sheet music along with audio
    '''
    global i, playing_state, audio_length, total_lines
    no_of_bars = total_lines
    if playing_state:
        while i < no_of_bars:
            
            #  CHANGE HOW THE IMAGE IS BEING IMPORTED
            bar.img = ImageTk.PhotoImage(Image.open('crop_' + str(i)+'.png'),master=top_frame)
            x = bar.canvas.create_image(1500/2, 100, image=bar.img, anchor = 'center')
            bar.canvas.update()
            #bar.canvas.itemconfig(bar.image_on_canvas, image = im3, mater = top_frame)
            #bar.canvas.itemconfig(x, image = im3)

        
            # im3 = ImageTk.PhotoImage(Image.open('crop_' + str(i)+'.png'),master=window)
            # Sheet_frame.image = im3
            # Sheet_frame.configure(image = im3)

            i+=1

            break

        Sheet_frame.after(int((audio_length/no_of_bars)*1000),display)
    else:
        return
        
def pause():
    '''Pauses audio file 
    '''
    global playing_state, midi_file, run, moving
    mixer.music.pause()
    playing_state = False 
    
    
    # ADD BAR PART OF PAUSE
    run= False
    moving = False

def resume():
    '''Resumes audio file 
    '''
    global playing_state, moving, run
    mixer.music.unpause()
    playing_state = True
    
    
    # ADD BAR PART OF RESUME
    run = True
    if moving == False:
        rect_bar.movement()
    moving = True
    
def play_midi():
    global midi_file, running_song
    playMidiFile(midi_file)
    running_song['text'] = midi_file

def external_device():
    global str_notes
    
    ext_midi = play_external.MidiSequence()
    ext_midi.notes2sequence(notes_str = str_notes)
    sequence=ext_midi.getSequence()
    #print(a)

    Synth = play_external.connectSynth()
    smallest_subdivision = 8
    bpm = 120; bps = bpm/60; sps = bps/smallest_subdivision
    for i in range(len(sequence[0])):
        (NoteON,NoteOFF) = ext_midi.play_external.getNote(i)
        printMessage(NoteON,NoteOFF) 
        if NoteON:
            Synth.note_on(note=NoteON, velocity=127)
        if NoteOFF:
            Synth.note_off(note=NoteOFF, velocity=127)
        time.sleep(sps)
    
# MAIN
# ADD ADDITIONAL GLOBAL VARIABLES
global run, moving, toStart
run = True
moving = False
toStart = False

   
#initializing variables
music_file = ''
playing_state = False
i = 0
audio_length = 0
midi_file = ''
total_lines = 0
str_notes = []

# insert BAR canvas object INTO FRAME
bar = ''



#Buttons
Upload_img = Image.open('Icons/upload.png') 
Upload_img = Upload_img.resize((50,50))
Upload_img = ImageTk.PhotoImage(Upload_img,master=window)
Upload_button = Button(bottom_frame, height = 50, image = Upload_img,bg = col1,command=upload)
Upload_button.place(x = 1500/8, y = 50, anchor ='center')

Play_img = Image.open('Icons/play.png') 
Play_img = Play_img.resize((50,50))
Play_img = ImageTk.PhotoImage(Play_img,master=window)
Play_button = Button(bottom_frame, height = 50, image = Play_img,bg = col1, command=lambda:[play(music_file, bar), display()])
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

Play_to_generated_midi = Button(middle_frame, text = ('Play Generated Midi'), font=("Arial",30),fg = 'black', command = play_midi)
Play_to_generated_midi.place(x = 1500/4, y = 50, anchor ='center')

Play_to_external_device = Button(middle_frame, text = ('Play to External Device'+'\n'+'(external device req)'), font=("Arial",30),fg = 'black', command = external_device)
Play_to_external_device.place(x = (1500/4)*3, y = 50, anchor ='center')

running_song = Label(bottom_frame_text,text ='Load',font=("Arial",25) ,fg = 'black')
running_song.place(x = (1500/2), y = 20, anchor ='center')



        


window.mainloop()
