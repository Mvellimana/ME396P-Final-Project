# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 12:25:30 2022

@author: Job Ramirez
"""
import time
import pygame
import pygame.midi

#Sample Melody on Lily Pond Format
Mario_Sequence_LP = "e'8 e'8 r8 e'8 r8 c'8 e'4 g'4 r4 g4 r4 c'4 r8 g8 r4 e4 r8 a8 r8 b8 r8 bes8 a4 g8 e'8 r8 g'8 a'4 f'8 g'8 r8 e'8 r8 c'8 d'8 b8 r8 r8"
smallest_subdivision = 8

def timeSignature(time_signature):
    if time_signature == '4/4':
        scale = smallest_subdivision
    return scale                
  
class MidiSequence:
    def __init__(self, **kwargs):
        # MIDI Note Degrees Dictionary
        degrees = 128; # Number of Notes on MIDI Communication (0-127)
        ref_freq = 440; ref_deg = 69; # 440 Hz = MIDI Note 69 
        # Following equal temperment division of 12 notes per octave
        freq = [round(ref_freq*2**((n-ref_deg)/12),2) for n in range(degrees)] 
        self.degree_dict = {freq[i]: i for i in range(len(freq))}
        self.degree_dict[-1] = '' # -1 will denote silence on voicing
        
        # Note Name  Dictionary
        if 'note_dictionary' in kwargs:
            self.note_dict = kwargs['note_dictionay']
        else: #default german notation
            freq = [-1, 16.35, 17.32, 18.35, 19.45, 20.6, 21.83, 23.12, 24.5, 25.96, 27.5, 29.14, 30.87, 32.7, 34.65, 36.71, 38.89, 41.2, 43.65, 46.25, 49, 51.91, 55, 58.27, 61.74, 65.41, 69.3, 73.42, 77.78, 82.41, 87.31, 92.5, 98, 103.83, 110, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185, 196, 207.65, 220, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392, 415.3, 440, 466.16, 493.88]
            notes =["r","c,,,", "des,,,", "d,,,", "ees,,,", "e,,,", "f,,,", "ges,,,", "g,,,", "aes,,,", "a,,,", "bes,,,", "b,,,", "c,,", "des,,", "d,,", "ees,,", "e,,", "f,,", "ges,,", "g,,", "aes,,", "a,,", "bes,,", "b,,", "c," , "des," , "d," , "ees," , "e," , "f," , "ges," , "g," , "aes," , "a," , "bes," , "b," , "c"  , "des"  , "d"  , "ees"  , "e"  , "f"  , "ges"  , "g"  , "aes"  , "a"  , "bes"  , "b", "c'" , "des'" , "d'" , "ees'" , "e'" , "f'" , "ges'" , "g'" , "aes'" , "a'" , "bes'" , "b'" ]
            self.note_dict = {notes[i]: freq[i] for i in range(len(notes))}

        # Establish number of voicings
        if 'polyphony' in kwargs:
            self.polyphony = kwargs['polyphony']
        else: # Assume default single melody instrument
            self.polyphony = 1
  
        # Create Seqeunce List
        self.midi_sequence = [[] for i in range(self.polyphony)]
        
    def notes2sequence(self, notes_str = Mario_Sequence_LP, voice = 1, time_signature = '4/4', **kwargs):
        voice -= 1 
        parsed_notes = notes_str.split(' ')
        for item in parsed_notes:
            
            #ctr = 0
            #for item[:-(ctr+2):-1].isalnum():
            #    ctr += 1
        
            # retrieve note info
            #note = item[:len(item)-ctr]
            #duration = int(item[:-(ctr+1):-1][::-1])
            note = item[:len(item)-1]
            duration = int(item[-1])
            #if not duration:
            #    duration  = 1
              
            # conver to MIDI notation
            degree = self.degree_dict[self.note_dict[note]]  # convert to MIDI Notation
             
            # scale duration according to time signature and beats per minute
            midi_duration = int(timeSignature(time_signature)/duration)
            #print(degree, note, midi_duration)  
            for i in range(midi_duration):
                self.midi_sequence[voice].append(degree)
                
    def getSequence(self):
        return self.midi_sequence
        
    def getNote(self, n, voice=1):
        n= int(n);   voice -= 1;
        noteOn = ''
        noteOff = ''
        if n == 0:
            noteOn = self.midi_sequence[voice][0]
            noteOff = ''
        elif n == len(self.midi_sequence[voice])-1:
            noteOff = self.midi_sequence[voice][n]
            
        elif n > len(self.midi_sequence[voice])-1:
            noteOn = ''
            noteOff = ''
        else:
            current_note  = self.midi_sequence[voice][n]
            previous_note = self.midi_sequence[voice][n-1]
            if  current_note == previous_note:
                noteOn = ''
            else:
                noteOn  = current_note
                noteOff = previous_note
    
        return noteOn,noteOff
       
def connectSynth():
    pygame.midi.init()
    # print the devices and use the last output port.
    for i in range(pygame.midi.get_count()):
        (interf,name,is_input,is_output,is_opened) = pygame.midi.get_device_info(i)
        print ('[{0}]'.format(i),interf, name, is_input, is_output, is_opened)

    selected_port = int(input('Select the port number: '))
    selected_channel = int(input('Select Channel (1 - 16): '))
    
    midi_out = pygame.midi.Output(selected_port, selected_channel)
    
    return midi_out  

def playSynth():
    pass
       
def closeSynth():
    pass
    
def printMessage(n,f):
    n = str(n); f = str(f)
    on = n +' '*(4-len(n))
    off = f +' '*(4-len(f))
    console_output = 'Note On: '+ on + 'Note Off :' + off
    print(console_output)

MarioLick = MidiSequence()
MarioLick.notes2sequence()
a=MarioLick.getSequence()

Synth = connectSynth()
bpm = 120; bps = bpm/60; sps = bps/smallest_subdivision
for i in range(len(a[0])):
    (NoteON,NoteOFF) = MarioLick.getNote(i)
    printMessage(NoteON,NoteOFF) 
    if NoteON:
        Synth.note_on(note=NoteON, velocity=127)
    if NoteOFF:
        Synth.note_off(note=NoteOFF, velocity=127)
    time.sleep(sps)

bpm = 60; bps = bpm/60; sps = bps/smallest_subdivision
for i in range(len(a[0])):
    (NoteON,NoteOFF) = MarioLick.getNote(i)
    printMessage(NoteON,NoteOFF) 
    if NoteON:
        #pass
        Synth.note_on(note=NoteON, velocity=127)
    if NoteOFF:
        #pass
        Synth.note_off(note=NoteOFF, velocity=127)
    time.sleep(sps)

# =============================================================================
# t_start = time.time()
# t = 0 
#  
# while t < 10:
#     if int(t % ssd) == 0:
#         T_sample = t//ssd
#         (NoteON,NoteOFF) = MarioLick.getNote(T_sample)
#         if NoteON:
#             Synth.note_on(note=NoteON, velocity=127)
#         if NoteOFF:
#             Synth.note_off(note=NoteOFF, velocity=127)
#         print(t); 
#     t = time.time() - t_start
#       
# 
# =============================================================================
       