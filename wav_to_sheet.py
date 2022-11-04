#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 20:17:32 2022

@author: dantegarcia
"""
# from mingus.containers import Note
# from mingus.containers import NoteContainer
# from mingus.containers import Bar
# import subprocess
# import os
import mingus.extra.lilypond as lilypond
from scipy.io import wavfile
from scipy import signal
import numpy as np

# testing commit
"""
Lilypond must be installed on your computer for the lilypond package to work
I had some issues with setup that took a while to figure it out. 
Let me know if you have issues, I can likely help! -Dante

This is just a first commit, it pretty much only works for the 'MaryHad3.wav' file.
I left some stuff out that I've been working on, and will commit it when it's functional
"""


# INPUTS
fs, data = wavfile.read('MaryHad3.wav')
bpw = 1; # input*1/4 = lost res note length if 1 beat per window, each window is 1/4 note (in 4/4), for now. so, only able to look at 1/4 beats or longer. need to try this for 1/8, 1/16, etc.
bpm = 60; #specify beats per minute

song_title = '"Mary Had a Little Lamb Test"'

# I copied this off the web. Sorry!
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx],idx

# List of notes and their associated frequency - will (likely) eventually turn this into a dictionary and include the last 3 octaves
freq = np.array([16.35, 17.32, 18.35, 19.45, 20.6, 21.83, 23.12, 24.5, 25.96, 27.5, 29.14, 30.87, 32.7, 34.65, 36.71, 38.89, 41.2, 43.65, 46.25, 49, 51.91, 55, 58.27, 61.74, 65.41, 69.3, 73.42, 77.78, 82.41, 87.31, 92.5, 98, 103.83, 110, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185, 196, 207.65, 220, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392, 415.3, 440, 466.16, 493.88])
notes = np.array(["c,,,", "des,,,", "d,,,", "ees,,,", "e,,,", "f,,,", "ges,,,", "g,,,", "aes,,,", "a,,,", "bes,,,", "b,,,",\
"c,,", "des,,", "d,,", "ees,,", "e,,", "f,,", "ges,,", "g,,", "aes,,", "a,,", "bes,,", "b,,",\
"c," , "des," , "d," , "ees," , "e," , "f," , "ges," , "g," , "aes," , "a," , "bes," , "b," ,\
"c"  , "des"  , "d"  , "ees"  , "e"  , "f"  , "ges"  , "g"  , "aes"  , "a"  , "bes"  , "b"  ,\
"c'" , "des'" , "d'" , "ees'" , "e'" , "f'" , "ges'" , "g'" , "aes'" , "a'" , "bes'" , "b'" ])

# =============================================================================
# # Future dictionary
# octaves = 5; start_freq = 16.35; 
# # Following equal temperment division of 12 notes per octave
# freq = [start_freq*2**(i/12) for i in range(octaves*12)] 
# notes =  ...
# note_map={}
# for i in range(octaves*12):
#     note_map[notes[i]]=[freq[i]]
# =============================================================================
    


#Windowing info calcs
bps = bpm/60;
window_length = round(fs/bps*bpw);
n_wndws = len(data)//window_length

# Spectrogram returns the SFFT of a specified block of time in our data
f, t, Sxx = signal.spectrogram(data,fs=fs,nperseg=window_length,noverlap=0, nfft=None)

# Only look at first 5 octaves - limit f to 500 Hz - this is for avoiding harmonics
f_lim = f[np.arange(500)]
Sxx = Sxx[np.arange(500),0:n_wndws]
Sxx_dB = 20*np.log10(abs(Sxx))

# Finding maximum magnitude/frequency for each time window
max_freq_idx = np.argmax(Sxx, axis=0)
max_freq_per_wndw = f[max_freq_idx]
max_freq_mag = np.amax(Sxx_dB, axis=0)
max_mag = max(max_freq_mag)

# Finding nearest note-frequency value to the frequency with max magnitude from spectrogram
note_f_val = np.array([], dtype=np.uint32)
note_f_idx = np.array([], dtype=np.uint32)
for ii,jj in enumerate(max_freq_per_wndw):
    val,idx = find_nearest(freq,jj)
    note_f_idx = np.append(note_f_idx,idx)
    note_f_val = np.append(note_f_val,val)

#string list of notes we want to play
notes_to_play = notes[note_f_idx]

# Only here for the last note of mary had a little lamb
# This will be changed and more processing code will be added
if (len(notes_to_play))%4 !=0:
    if (len(notes_to_play))%4 == 3: #3 beats played, one left - 3rd not is half note
        notes_to_play[-1] += '2'
    elif (len(notes_to_play))%4 == 2: #2 beats played, 2 left - 2nd is 3 beats, or 2.
        notes_to_play[-1] += '2.'
    elif (len(notes_to_play))%4 == 1: #1 beats played, 3 left - 1st is full note
        notes_to_play[-1] += '1'

# To see what notes will be played
print(notes_to_play)

#Setting up input to lilypond
str_notes = ' '.join(np.array(notes_to_play))
bar1 = '\header{\n  title = '+ song_title + '\n} \n\n' + \
       '{ \n  \ '.strip() + 'numericTimeSignature\n  \ '.strip() + \
       'time 4/4\n  ' + str_notes + '\n}'
       
# Exporting sheet music to pdf in your current directory       
lilypond.to_pdf(bar1, "testing1234")







