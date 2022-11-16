#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 14:35:25 2022

@author: dantegarcia
"""

import wav_to_sheet as ws

str_notes, total_lines, seconds_per_line, note_dict, bar, bpm = \
    ws.WavToSheet('MarioGuitar.wav')
    
