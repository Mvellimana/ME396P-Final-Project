# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 13:55:27 2022

@author: Job
"""

import pygame
import pygame.midi


def playMidiFile(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def pauseInstrument():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()

def resumeInstrument():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()   
