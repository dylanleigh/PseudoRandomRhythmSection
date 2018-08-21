#
# Dylan Leigh August 2018
# FIXME frontmatter goes here
# 

import sys
import random
from copy import deepcopy

from music21.instrument import Piano, AcousticBass, HiHatCymbal
from music21.roman import RomanNumeral
from music21.stream import Part, Measure, Score
from music21.converter.subConverters import ConverterMusicXML
from music21.note import Note, Rest
from music21.chord import Chord
#from music21.interval import Interval


# NOTE: This progression generator was nicked from an earlier project
# to generate techno :)
# TODO: Add more chord types
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
   # FIXME define output file on cli...
   sys.exit('Usage: python autobebop.py; musescore /tmp/music21/output.xml\n')


def quaver_length():
   '''Return a note length averaging to an eighth note'''
   return random.choice((0.25,0.25, 0.5,0.5,0.5,0.5, 1.0))


def add_piano_riff(roman, duration, piano):
   '''Given a Roman chord, duration in eighths/quavers and a keyboard
      part, generate a riff and add it to the keyboard part'''

   # Add piano part
   filled = 0
   while filled < duration:
      # NOTE: higher chance to rest if on beat = more syncopated rhythm to piano
      if random.randint(0, 1 + filled%2 + filled%4):
         # XXX: Must deepcopy, do not change original or it will break bassline
         chord = Chord(deepcopy(roman.pitches))

         # TODO ending riff at end of song

         # invert chord randomly, root inversion twice as likely as others
         max_inv=len(chord.pitches)
         chord.inversion(random.randint(0,max_inv)%max_inv)

         # Randomly hold notes for longer if we have longer before
         # the next chord change
         max_length = min(duration-filled, 4)      # Cap at 1/2 bar
         length = random.randint(1,max_length)
         chord.quarterLength = length/2.0      # length is in eighths

         # Add an extra root note 1 octave lower
         root = deepcopy(chord.root())
         root.octave -= 1
         chord.add(root)

         piano.append(chord)
         filled += length
      else:
         piano.append(Rest(quarterLength=0.5))
         filled += 1


def add_bass_walk(roman, duration, bass):
   '''Given a Roman chord, duration in eights/quavers and a bass part,
      generate a walking bass up and down the chord notes.
      Note although duration is in eigths, the bassline will be
      quarter notes, on beat.'''

   # Create quarter note walking bassline, on chord notes
   chord_notes = [str(p) for p in roman.pitches]
   # add reversed tail of walk (but don't repeat the top or bottom)
   walk_notes = chord_notes + chord_notes[-2:0:-1]
   for pos in range(0, duration, 2):   # 2 as we want quarter notes, duration is in eigths
      # TODO ending riff if last chord
      note = Note(walk_notes[pos/2%len(walk_notes)])  # Wrap back to start
      note.octave -= 2
      bass.append(note)


def generate_song():
   '''Generate a random song and return as a Music21 score'''
   # Start with a blank score
   score = Score()
   # TODO: Add swing rhythm indicator outside musescore

   # Add tracks/intstruments - names etc will be set automatically
   piano = Part()
   piano.insert(0, Piano())
   score.insert(0,piano)

   bass = Part()
   bass.insert(0, AcousticBass())
   score.insert(0,bass)

   #hihat = Part()   TODO

   # Get a random progression
   prog = ProgressionGenerator()
   prog.generate(15)       # TODO longer, make CLI opt

   # Go through the progression, adding a comp for each chord
   for chord_choice in prog.chords:
      # Duration = eights until the next chord change.
      # longer on "important" chords (I,IV,V)
      if chord_choice in ('I', 'IV', 'V', 'V7'):
         duration = random.choice((8,8,8,8,10,10,12,12,14,16))
      else:
         duration = random.choice((2,4,4,4,6,6,8,8,8,8))

      roman = RomanNumeral(chord_choice)   # Convert string into a generic Roman I/IV/etc chord

      add_piano_riff(roman, duration, piano)
      add_bass_walk(roman, duration, bass)
      # TODO drum part

   return score


# start main function
if __name__ == '__main__':
   print("musescore " + generate_song().write("musicxml"))
