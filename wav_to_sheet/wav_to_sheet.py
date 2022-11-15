#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 20:17:32 2022

@author: dantegarcia
"""

import mingus.extra.lilypond as lilypond
from scipy.io import wavfile
from scipy import signal
import numpy as np
from scipy import fftpack as ft
import matplotlib.pyplot as plt

def WavToSheet(filename):
    # INPUTS
    #filename = 'Mario_Guitar_120bpm_5.wav'
    fs, data = wavfile.read(filename) #Mario_Guitar_100bpm_1
    bpw = 1/2; # input*1/4 = lost res note length if 1 beat per window, each window is 1/4 note (in 4/4), for now. so, only able to look at 1/4 beats or longer. need to try this for 1/8, 1/16, etc.
    bpm = 120; #specify beats per minute
    
    song_title = 'filename'
    
    
    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx],idx
    
    
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
    
    
    f, t, Sxx = signal.spectrogram(data,fs=fs,nperseg=window_length,noverlap=0, nfft=None)
    
    # Only look at first 5 octaves - dodging harmonics, for now
    f_lim = np.array([i for i in f if i < 500])
    lim = len(f_lim)
    Sxx = Sxx[np.arange(lim),0:n_wndws]
    Sxx_dB = 20*np.log10(abs(Sxx))
    max_freq_idx = np.argmax(Sxx, axis=0)
    max_freq_per_wndw = f[max_freq_idx]
    max_freq_mag = np.amax(Sxx_dB, axis=0)
    max_mag = max(max_freq_mag)
    
    note_f_val = np.array([], dtype=np.uint32)
    note_f_idx = np.array([], dtype=np.uint32)
    for ii,jj in enumerate(max_freq_per_wndw):
        val,idx = find_nearest(freq,jj)
        note_f_idx = np.append(note_f_idx,idx)
        note_f_val = np.append(note_f_val,val)
            
            
    
    notes_to_play_8 = notes[note_f_idx]
    notes_to_play = notes_to_play_8.copy()
    
            
    for i,val in enumerate(notes_to_play):
        if max_freq_mag[i] <= max_mag - 33:
            notes_to_play[i] = 'r'
            
    notes_to_play = [i+'8' for i in notes_to_play]
    notes_to_play.extend(['r8']*(len(notes_to_play)%8))
    
    
    # Creating lists that contain the index locations of rest groups and the number of rests in the group
    # There has to be a better way to do this!
    rest_idx_lst = [i for i,val in enumerate(notes_to_play) if val == 'r8'] 
    rest_idx_lst_tmp = rest_idx_lst.copy()
    rest_grp_idx_lst,rests_in_grp_lst = [],[]
    for i,val in enumerate(rest_idx_lst_tmp):
        cntr, b = 1, 1
        while b and i+cntr < len(rest_idx_lst_tmp):
            if val == 'pass':
                b = 0
            elif val + cntr == rest_idx_lst_tmp[i+cntr]:
                rest_idx_lst_tmp[i+cntr] = 'pass'
                if i+cntr == len(rest_idx_lst_tmp) - 1 and cntr != 1:
                    rest_grp_idx_lst.append(val), rests_in_grp_lst.append(cntr+1)
                cntr += 1
            else:
                rest_grp_idx_lst.append(val), rests_in_grp_lst.append(cntr)
                b = 0
        if i == len(rest_idx_lst_tmp) - 1 and rest_idx_lst_tmp[i] != 'pass':
            rest_grp_idx_lst.append(val), rests_in_grp_lst.append(cntr)
    
    # Handles when there are rest groups more than three 8th notes long
    # This creates rest groups of only 3 8th's or lower
    for i,ival in enumerate(rests_in_grp_lst):
        if ival > 3:
            x,y = ival//3,ival%3 # floor, remainder
            elements_to_add = x
            rests_in_grp_lst[i] = 3
            for j in range(0,x):
                rest_grp_idx_lst.insert(i+j+1,rest_grp_idx_lst[i+j]+3)
                if j == x-1:
                    rests_in_grp_lst.insert(i+j+1,y)
                else:
                    rests_in_grp_lst.insert(i+j+1,3)    
    
    #rest_grp_idx_lst, rests_in_grp_lst
    
    #Handling rests
    for ii,ival in enumerate(rest_grp_idx_lst):
        if ival%2: # if the index is odd
            if rests_in_grp_lst[ii] == 1:
                notes_to_play[ival-1] = notes_to_play[ival-1][0:-1] + '4'
                notes_to_play[ival] = 'remove'
            if rests_in_grp_lst[ii] == 2:
                notes_to_play[ival-1] = notes_to_play[ival-1][0:-1] + '4'
                notes_to_play[ival] = 'remove'
            if rests_in_grp_lst[ii] == 3:
                notes_to_play[ival-1] = notes_to_play[ival-1][0:-1] + '4'
                notes_to_play[ival] = 'remove'
                notes_to_play[ival+1] = 'remove'
                notes_to_play[ival+2] = notes_to_play[ival+2][0:-1] + '4'
        else: # if the index is even
            if rests_in_grp_lst[ii] == 2:
                notes_to_play[ival] = 'remove'
                notes_to_play[ival+1] = notes_to_play[ival+1][0:-1] + '4'
            if rests_in_grp_lst[ii] == 3:
                notes_to_play[ival] = 'remove'
                notes_to_play[ival+1] = notes_to_play[ival+1][0:-1] + '4'
    
    notes_to_play = [i for i in notes_to_play if i != 'remove']
    
    
    
    # Checking Spectrum with FFT
    if 0:
        window = 35
        i1 = window_length*(window-1)
        i2 = i1 + window_length
        sig = data[i1:i2]
        N = len(sig)
        counts = np.arange(N) # array from 0 to N-1
        time = counts/fs # time array
        freq = np.linspace(0.0, fs/2, N//2) #use // to return int
        sig_fft = ft.fft(sig)
        mag = np.abs(sig_fft) 
        
        # plot time-series and frequency response of unfiltered signal
        fig, ax1 = plt.subplots(2)
        ax1[0].plot(time,sig)
        ax1[0].set(title='time (s) vs. amplitude - unfiltered')
        ax1[1].plot(freq, 2.0/N * np.abs(mag[:N//2]))
        ax1[1].set(title='frequency (Hz) vs amplitude',xlim=[0,1000])
        plt.tight_layout()
        plt.show()
        
        test_max_idx = np.argmax(mag, axis=0)
        print(freq[test_max_idx])
        
        
    for idx,n in enumerate(notes_to_play):
        print(str(idx+1) + ': ' + n)
    
    str_notes = ' '.join(np.array(notes_to_play))
    
    # Testing txt file input for lilypond string
    with open("lilypond_string_input_1.txt","r") as f:
        str1 = f.read()
    with open("lilypond_string_input_2.txt","r") as f:
        str2 = f.read()
        
    bar2 = str1 + str_notes + str2
    lilypond.to_pdf(bar2, "bar2test")
    lilypond.to_png(bar2, "bar2test")
    
    
    total_lines = int(len(notes_to_play_8)/16)
    seconds_per_line = 8*60/bpm
    
    # This file also creates a png/pdf of sheet music and a midi file
    # It requires the input of a wav file, and two .txt files that contain lilypond info
    
    return str_notes, total_lines, seconds_per_line
