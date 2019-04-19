# Mastropiero
# by Martín del Río (lartu.net)

#!/usr/bin/python3
import sys
from pysine import sine
import re
from math import floor

if len(sys.argv) < 2:
    print("Usage: ")
    print("$ python mastropiero.py <sourceFile>")
    exit(1)
filename = sys.argv[1]


characters = []
charCount  = []
scales = [[293.3,  330,   352,  391.1,   440,   488.9,  264], #Dorien
          #[352, 396, 440, 488.89, 264, 293.33, 330], #lydian
          #[264, 297, 330, 352, 396, 440, 495], #ionian
          #[396, 445.50, 495, 264, 297, 330, 356.40], #mixolydian
          #[440, 495, 264, 293.33, 330, 352, 396], #aeolian
         ] 

# Load the source file
fileContents = open(filename, "r").read()

# Count characters in source file
for char in fileContents:
    if char in characters:
        index = characters.index(char)
        charCount[index] = charCount[index] + 1
    else:
        characters.append(char)
        charCount.append(1)

# Sort characters by appearance
characters = [x for _, x in sorted(zip(charCount,characters), reverse=True)]
charCount = (sorted(charCount, reverse=True))

# Print them
print("")
print("Characters found in " + filename + ":")
for i in range(0, len(characters)):
    char = characters[i]
    if char == "\n":
        char = "\\n"
    elif char == "\t":
        char = "\\t"
    print("\033[1;32m" + char + "\033[0m " + "(" + str(charCount[i]) + ") ", end='')
    if (i+1) % 5 == 0 or i == len(characters) - 1:
        print("")
print("")

# Associate each character with a note
song = []
noteNum = 0
for char in fileContents:
    if noteNum % 32 == 0:
        noteFrequencies = scales[ord(char) % len(scales)]
    index = characters.index(char) % len(noteFrequencies)
    note = noteFrequencies[index]
    song.append(note)
    noteNum = noteNum + 1
    
# Assign each note a duration
noteLength = []
patternGroups = [[[1, 0.5, 0.5, 1, 1], [1, 0.5, 0.5, 1, -1]],
                  [[1, 1, 2], [2, 2], [1, 1, 1, -1], [2, 1, -1], [1, -1, 1, -1]],
                  [[1, 0.5, 0.5, 2], [2, 0.5, 0.5, 1], [1, -0.5, 0.5, 2], [2, -0.5, 0.5, 1], [1, 0.5, 0.5, -2], [2, 0.5, 0.5, -1]],
                  [[4], [3, -1]],
                 ]
    #, [4], , [1, 1, 1, 1], [3, 1], [1, 3]
currentPattern = []
patternsUsed = 0
for note in song:
    if patternsUsed % 4 == 0:
        patterns = patternGroups[floor(note % len(patternGroups))]
    if len(currentPattern) == 0:
        currentPattern = patterns[floor(note % len(patterns))].copy()
        patternsUsed = patternsUsed + 1
    if song.index(note) == len(song) - 1:
        noteLength.append(1)
    else:
        noteLength.append(currentPattern.pop(0) / 4)
    
# Print how long will the song be
songLength = 0
for l in noteLength:
    songLength = songLength + l;
print("Total song length: " + str(songLength / 30) + " minutes")
    
# Play the song
noteNum = 1
for note in song:
    noteDuration = noteLength[noteNum - 1]
    if noteDuration < 0:
        noteDuration = noteDuration * -1
        note = 0
    sine(frequency = note, duration=noteDuration)
    noteNum = noteNum + 1
