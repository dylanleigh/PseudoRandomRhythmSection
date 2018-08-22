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
#from music21.interval import Interval TODO for more varied fills
from music21.volume import Volume
from music21.harmony import Harmony    # FIXME use to print chord symbols


# TODO: Replace all this with a matrix of from-chord -> relative-probability -> to-chord
# TODO: Add more chord types
class ProgressionGenerator:
   def __init__(self):
      self.chords = ['V7']    # Work backwards from V7 - a ending riff on I will be added after

   def __str__(self):
      return str(self.chords)

   def before_Imaj7(self):
      return random.choice(['IVmaj7','IVmaj7','V7','V7','viio'])

   def before_iim7(self):
      return random.choice(['Imaj7','iiim7','IVmaj7','vim7'])

   def before_iiim7(self):
      return random.choice(['Imaj7','iim7','IVmaj7'])

   def before_IVmaj7(self):
      return random.choice(['Imaj7','iiim7','vim7'])

   def before_V7(self):
      return random.choice(['Imaj7','iim7','IVmaj7','vim7'])

   def before_vim7(self):
      return random.choice(['Imaj7','iiim7','V7'])

   def before_viio(self):
      return random.choice(['Imaj7','iim7','IVmaj7'])

   def generate(self, min_length=2):
      curr = self.chords[0]
      while len(self.chords) < min_length or curr != 'Imaj7':
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

         # invert chord randomly, root inversion twice as likely as others
         max_inv=len(chord.pitches)
         chord.inversion(random.randint(0,max_inv)%max_inv)

         # TODO try randomly ommitting some chord notes

         # Randomly hold notes for longer if we have longer before
         # the next chord change
         max_length = min(duration-filled, 4)      # Cap at 1/2 bar
         length = random.randint(1,max_length)
         chord.quarterLength = length/2.0      # length is in eighths

         # Add an extra root note 1 octave lower
         root = deepcopy(chord.root())
         root.octave -= 1
         chord.add(root)

         chord.volume = Volume(velocity=16,velocityIsRelative=False)
         piano.append(chord)
         filled += length
      else:
         piano.append(Rest(quarterLength=0.5))
         filled += 1


def add_piano_closing(roman, duration, piano):
   '''Generate a closing riff and add it to the keyboard part'''
   filled = 0
   length_weight = 2    # Longer notes later in the bar
   root = roman.root()  # Root pitch of the chord (NOT a note object)
   while filled < duration:
      # TODO DRY with other piano func
      chord = Chord(deepcopy(roman.pitches))

      # invert chord randomly, root inversion twice as likely as others
      max_inv=len(chord.pitches)
      chord.inversion(random.randint(0,max_inv)%max_inv)

      # Add an extra root note 1 octave lower
      root = deepcopy(chord.root())
      root.octave -= 1
      chord.add(root)
      # TODO above same procedure as main riff func, but we should
      # make more fancy

      # Rhythm similar to bass method below
      length = min(random.randint(1,length_weight),duration-filled) # cap at time left
      chord.quarterLength = length/2.0

      piano.append(chord)
      filled += length
      length_weight += length # Longer notes later in the bar


def add_bass_walk(roman, duration, bass):
   '''Given a Roman chord, duration in eights/quavers and a bass part,
      generate a walking bass up and down the chord notes.
      Note although duration is in eigths, the bassline will be
      quarter notes, on beat.'''

   chord_notes = [str(p) for p in roman.pitches]
   # add reversed tail of walk (but don't repeat the top or bottom)
   walk_notes = chord_notes + chord_notes[-2:0:-1]
   for pos in range(0, duration, 2):   # 2 as we want quarter notes, duration is in eigths
      note = Note(walk_notes[pos/2%len(walk_notes)])  # Wrap back to start
      note.octave -= 2
      bass.append(note)


def add_bass_closing(roman, duration, bass):
   '''Generate a closing riff for the bassline, given chord and
      duration in eighths'''
   filled = 0
   length_weight = 2    # Longer notes later in the bar
   root = roman.root()  # Root pitch of the chord (NOT a note object)
   while filled < duration:
      note = Note(deepcopy(root))
      length = min(random.randint(1,length_weight),duration-filled) # cap at time left
      note.quarterLength = length/2.0

      note.octave -= 2
      bass.append(note)
      filled += length
      length_weight += length # Longer notes later in the bar


def generate_song():
   '''Generate a random song and return as a Music21 score'''
   # Start with a blank score
   score = Score()
   # TODO: Add swing rhythm indicator without having to do it manually
   # in musescore (how to with music21?)

   # Add tracks/intstruments - names etc will be set automatically
   piano = Part()
   piano.insert(0, Piano())
   score.insert(0,piano)

   bass = Part()
   bass.insert(0, AcousticBass())
   score.insert(0,bass)

   #hihat = Part()   TODO drum kit

   # Get a random progression
   prog = ProgressionGenerator()
   prog.generate(15)  # 15 changes tends to ~= 1 page of output   # TODO make CLI opt

   # Go through the progression, adding a comp for each chord
   for chord_choice in prog.chords:
      # FIXME add Harmony/Chord Symbol to score!

      # Duration = eights until the next chord change.
      # at least 1 bar on "important" chords (I,IV,V)
      if chord_choice in ('Imaj7', 'IVmaj7', 'V7'):
         duration = random.choice((8,8,8,8,10,10,12,12,14,16))
      else: # 1 bar or less on "minor" (pun intended) chords
         duration = random.choice((2,4,4,4,6,6,8,8,8,8))

      roman = RomanNumeral(chord_choice)   # Convert string into a generic Roman I/IV/etc chord

      add_piano_riff(roman, duration, piano)
      add_bass_walk(roman, duration, bass)
      # TODO drum part

   # ending riff on last bar
   add_piano_closing(RomanNumeral('Imaj7'), 8, piano)
   add_bass_closing(RomanNumeral('Imaj7'), 8, bass)
   return score


# start main function
if __name__ == '__main__':
   print("musescore " + generate_song().write("musicxml"))
