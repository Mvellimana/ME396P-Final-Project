#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 14:35:25 2022

@author: dantegarcia
"""

def myFunc(a):
    b = a + 1
    return b

import wav_to_sheet as ws

ws.WavToSheet('Mario_Guitar_120bpm_5.wav')