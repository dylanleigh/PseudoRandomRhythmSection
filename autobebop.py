#
# Dylan Leigh August 2018
# TODO frontmatter goes here
# 

import fileinput
import sys
import random

from music21 import note
from music21.instrument import Piano, AltoSaxophone
from music21.stream import Part, Measure, Score
from music21.converter.subConverters import ConverterMusicXML

DEBUG=True

class Progression:
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


def init_song():
   '''Initialise music21 with a new Sax/Piano score and return it.'''
   score = Score()

   # Add tracks/intstruments for SATB - names etc will be set automatically
   piano_p = Part()
   piano_p.insert(0, Piano())

   alto_p = Part()
   alto_p.insert(0, AltoSaxophone())

   return score


def generate_song():
   '''Generate a random song and return as a Music21 score'''
   # Initialise the score
   score = init_song()

   # FIXME while song length too short
   # Get a progression

   return score


# start main function
if __name__ == '__main__':
   generate_song().write("musicxml")
