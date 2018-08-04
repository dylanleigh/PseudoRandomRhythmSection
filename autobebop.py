#
# Dylan Leigh August 2018
# TODO frontmatter goes here
# 

import fileinput
import sys
import random

from music21.instrument import Piano, AltoSaxophone
from music21.roman import RomanNumeral
from music21.stream import Part, Measure, Score
from music21.converter.subConverters import ConverterMusicXML
from music21.note import Note, Rest
from music21.chord import Chord


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


def generate_song():
   '''Generate a random song and return as a Music21 score'''
   # Start with a blank score
   score = Score()

   # Add tracks/intstruments - names etc will be set automatically
   piano = Part()
   piano.insert(0, Piano())
   score.insert(0,piano)

   alto = Part()
   alto.insert(0, AltoSaxophone())
   score.insert(0,alto)

   # Get a random progression
   prog = ProgressionGenerator()
   prog.generate(20)

   # Go through the progression, adding a chord and a note
   for chord in prog.chords:
      duration = random.choice((1,2,2,3,4,4,4,5,6))      # beats until chord change

      # Add chord to piano part
      roman = RomanNumeral(chord)   # Convert string into a generic chord object
      roman.quarterLength = 1 # One per beat TODO mix up rhythm a bit
      for pos in range(0, duration):
         piano.append(Chord(roman))

      # Create melody based on eighth-notes
      for pos in range(0, duration * 2):

         # Get chord notes, add scale notes, these are our potential notes
         chord_notes = [str(p) for p in roman.pitches]
         notes = chord_notes + ['C','D','E','F','G','A','B']   # FIXME ugh

         # Add a note or a rest
         # FIXME we choose rest here because we want to weight certain
         # notes, durations etc.
         if random.randint(0,2):
            note = Note(random.choice(notes))
            note.quarterLength = 0.5
            alto.append(note)
         else:
            alto.append(Rest(quarterLength=0.5))

   return score


# start main function
if __name__ == '__main__':
   print(generate_song().write("musicxml"))
