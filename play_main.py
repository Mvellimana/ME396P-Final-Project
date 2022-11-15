# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 13:55:27 2022

@author: Job
"""

import time
from midiutil import MIDIFile
import pygame
import pygame.midi


# Connect to synth Example

def connectSynth():
    pygame.midi.init()
    # print the devices and use the last output port.
    for i in range(pygame.midi.get_count()):
        (interf,name,is_input,is_output,is_opened) = pygame.midi.get_device_info(i)
    print ('[{0}]'.format(i),interf, name, is_input, is_output, is_opened)

    selected_port = int(input('Select the port number: '))

    # You could also use this to use the default port rather than the last one.
    # default_port = pygame.midi.get_default_output_id()

    midi_out = pygame.midi.Output(selected_port, 0)

    # select an instrument.
    instrument = 19 # general midi church organ.
    midi_out.set_instrument(instrument)

    # play a note.
    midi_out.note_on(note=62, velocity=127)
    midi_out.note_off(note=62, velocity=0)

    # sleep for a bit, and play another higher pitched note.
    time.sleep(0.5)
    midi_out.note_on(note=80, velocity=127)
    midi_out.note_off(note=80, velocity=0)
    time.sleep(0.5)

    # play a note for longer.
    midi_out.note_on(note=62, velocity=127)
    time.sleep(1.0)
    midi_out.note_off(note=62, velocity=0)

    pygame.midi.Output.close(midi_out)


          
def save2midi(sequence, filename, tempo = 60):
    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 1    # In beats
    # tempo    = 60   # In BPM
    volume   = 100  # 0-127, as per the MIDI standard
    
    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                          # automatically)
    MyMIDI.addTempo(track, time, tempo)
    
    for i, pitch in enumerate(sequence):
        MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)
    
    filename += '.midi'
    with open(filename, "wb") as output_file:
        MyMIDI.writeFile(output_file)
        


def playMidiFile(filename):
    pygame.mixer.init()
    pygame.mixer.music.load('MidiFileTest.midi')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        print('Still playing :)')
        time.sleep(1)
        
save2midi([64, 64, 64, 0, 60, 64, 67, 55],'MidiFileTest')

playMidiFile('MidiFileTest')

#connectSynth()
