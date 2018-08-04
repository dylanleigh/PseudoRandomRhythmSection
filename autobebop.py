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
from music21.note import Note


DEBUG=True     # FIXME rm these


class ProgressionGenerator:
   def __init__(self):
      self.chords = ['I']    # Work backwards from I

   def __str__(self):
      return str(self.chords)

   def before_I(self):
      path = random.randint(0,1)
      if path == 1:
         return random.choice(['IV','V','viio'])
      else:
         return random.choice(['IV','V'])

   def before_ii(self):
      return random.choice(['I','iii','IV','vi'])

   def before_iii(self):
      return random.choice(['I','ii','IV'])

   def before_IV(self):
      return random.choice(['I','iii','vi'])

   def before_V(self):
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



   return score


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
   if DEBUG:
      print('Progression Chords: ', prog.chords)

   # Go through the progression, adding a chord and a note
   for chord in prog.chords:
      duration = 4      # 4 beats per chord TODO mix this up a bit

      # Add to piano part
      roman = RomanNumeral(chord)   # Convert string into a generic chord object
      roman.quarterLength = duration
      piano.append(roman)

      # Create melody based on eighth-notes
      for pos in range(0, duration * 2):
         notes = [str(p) for p in roman.pitches]    # TODO expand potential notes
         note = Note(random.choice(notes))
         note.quarterLength = 0.5   # FIXME rests and mix up duration
         alto.append(note)

   return score


# start main function
if __name__ == '__main__':
   print(generate_song().write("musicxml"))
