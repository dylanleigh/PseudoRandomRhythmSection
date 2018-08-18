#
# Dylan Leigh August 2018
# TODO frontmatter goes here
# 

import fileinput
import sys
import random

from music21.instrument import Piano, AcousticBass
from music21.roman import RomanNumeral
from music21.stream import Part, Measure, Score
from music21.converter.subConverters import ConverterMusicXML
from music21.note import Note, Rest
from music21.chord import Chord
#from music21.interval import Interval


class ProgressionGenerator:
   def __init__(self):
      self.chords = ['I']    # Work backwards from I

   def __str__(self):
      return str(self.chords)

   def before_I(self):
      return random.choice(['IV','IV','V','V','V7','V7','viio'])

   def before_ii(self):
      return random.choice(['I','iii','IV','vi'])

   def before_iii(self):
      return random.choice(['I','ii','IV'])

   def before_IV(self):
      return random.choice(['I','iii','vi'])

   def before_V(self):
      return random.choice(['I','ii','IV','vi'])

   def before_V7(self):
      return random.choice(['I','ii','IV','vi'])

   def before_vi(self):
      return random.choice(['I','iii','V'])

   def before_viio(self):
      return random.choice(['I','ii','IV'])

   def generate(self, min_length=2):
      curr = self.chords[0]
      while len(self.chords) < min_length or curr != 'I':
         func = getattr(self, "before_%s" % curr)
         curr = func()
         self.chords.insert(0, curr)

# misc functions

def abort_with_usage():
   '''Abort with a usage message to STDERR'''
   sys.exit('Usage: autobebop.py > music.mxl\n')


def quaver_length():
   '''Return a note length averaging to an eighth note'''
   return random.choice((0.25,0.25, 0.5,0.5,0.5,0.5, 1.0))


def generate_song():
   '''Generate a random song and return as a Music21 score'''
   # Start with a blank score
   score = Score()

   # Add tracks/intstruments - names etc will be set automatically
   piano = Part()
   piano.insert(0, Piano())
   score.insert(0,piano)

   bass = Part()
   bass.insert(0, AcousticBass())
   score.insert(0,bass)

   # Get a random progression
   prog = ProgressionGenerator()
   prog.generate(15)       # TODO longer, make CLI opt

   # Go through the progression, adding a comp for each chord
   for chord_choice in prog.chords:
      duration = random.choice((2,4,4,6,8,8,8,10,12))  # eigths until chord change
      roman = RomanNumeral(chord_choice)   # Convert string into a generic Roman I/IV/etc chord

      # Add piano part
      filled = 0
      while filled < duration:
         if random.randint(0,2):
            chord = Chord(roman.pitches)
            # Randomly hold notes for longer if we have longer before
            # the next chord change
            length = random.randint(1,duration-filled)
            chord.quarterLength = length/2.0      # length is in eighths
            piano.append(chord)
            filled += length
         else:
            piano.append(Rest(quarterLength=0.5))
            filled += 1

      # Create quarter note walking bassline
      for pos in range(0, duration, 2):   # 2 as we want quarter notes, duration is in eigths
         # Walk up and down chord notes
         chord_notes = [str(p) for p in roman.pitches]
         # FIXME add reversed tail of walk here
         note = Note(chord_notes[pos%len(chord_notes)])  # Wrap back to start
         note.octave -= 2
         bass.append(note)

         # FIXME ending if last chord

   return score


# start main function
if __name__ == '__main__':
   print(generate_song().write("musicxml"))
