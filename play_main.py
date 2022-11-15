# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 13:55:27 2022

@author: Job
"""
import time
import pygame
import pygame.midi


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
