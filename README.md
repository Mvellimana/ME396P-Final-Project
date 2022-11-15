# SynMusic
_**A simple music transcriptor and reproducer using SciPy**_
## How To Use It!
#### 1. Install the Lily music engraving environment 
  * Lily Pond is a sheet music compiler and is needed to visually display music in our program. Follow the instruction in [Lily Pond website](https://lilypond.org/download.html)
#### 2. Install the necesary external python packages, more information on their respective documenation websites (listed on our references)
  * Tool and library for manipulating LilyPond files 
    > pip install python-ly
  * Package for creating MIDI format files 
    > pip install MIDIUtil
  

### Representing Music Visually 
Although music is a sonic phenomena, there are multiple ways to suncintly depict it graphically. Sheet music is one of them and it allows to represent the arrangement of pitches over time in staff notation. It uses an array of symbols and codes to precisely (but not necesarly intuitively) convey the fundamental elements of a piece of music, namely, pitch, rythm , dynamics, and timbre.

![image](https://user-images.githubusercontent.com/20881669/199405616-928f35ca-6f92-4c2d-901e-33b310f2c60a.png)


![Simple Music Notation Elements](https://user-images.githubusercontent.com/20881669/199398114-b406ef6f-548c-4a37-99ca-99a2b33f67b5.png)



### Playing to an Electronic Musical Instrument
#### MIDI Communication

## Signal Processing: From input to outputs
### Identifying Musical Elements
#### Pitch and Octave range
#### Rythmic Patterns
#### 

### Creating a Music Player GUI
The goal is to create a GUI that can control the audio input and output (with play, pause , resume buttons) and to display an animated sheet music that highlights the notes that are currently played.

## Dependancies :
 - [Tkinter](https://docs.python.org/3/library/tkinter.html): to create the music player interface
 - [Pygame](https://www.pygame.org/wiki/about): to control audio file
 - [MIDIUtil](https://pypi.org/project/MIDIUtil/): to save MIDI file
 
##  References
- Music Engraving Program: [LilyPond](http://lilypond.org/doc/v2.22/Documentation/learning/simple-notation)
- Python Lyli Pond Object Format Package: [python-ly](https://pypi.org/project/python-ly/)
- Basic of the MIDI Protocol: [MIDI Tutorial](https://www.cs.cmu.edu/~music/cmsip/readings/MIDI%20tutorial%20for%20programmers.html) 
- Notes to Midi Note Mapping: [Midi Note Numbers and Center Frequencies](https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies)

