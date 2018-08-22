
:::::::::::::::::::::::::
PseudoRandomRhythmSection
:::::::::::::::::::::::::

Dylan Leigh - August 2018

Generates a pseudorandom chord progression and piano/bass comp to go
with it; outputs a score in MusicXML with all parts and chord symbols.
Ideal for practicing improvisation or ideas for composition.

Installation/Requirements
=========================

Other than Python the only hard requirement is the Music21 library
http://web.mit.edu/music21/ which is used for writing the MusicXML and
performing chord inversions and similar operations.

A pip requirements file is provided, and it is recommended that
Virtualenv or a similar system be used for a clean environment::

   virtualenv prrs
   cd prrs
   . bin/activate
   git clone http://git/TODO
   pip install -r requirements.txt

Usage
=====

The file to save to must be specified as an argument. It can then be
opened with any MusicXML software such as Musescore::

   $ python prrs.py output.xml
   $ musescore output.xml

A one-liner::
   $ python prrs.py output.xml --show-symbols && musescore output.xml &

**Warning: The output file will be clobbered if it already exists.**

For full commandline options use --help.

Algorithms
==========

(This may change as improvements are made)

To generate the chord progression, PRRS puts a V7 and Imaj7 at the end
and then works backwards, making a weighted random choice between
chords that tend to resolve to the "current" chord. For example::

      I                 V     I
      I           ii    V     I
      I     vi    ii    V     I

Then the actual notes are generated working forwards. First a duration
is chosen for the current chord, then for each instrument a function
is called to generate the part for that instrument until the next
chord change. Chords that are more cadentially significant are more
likely to have a longer duration.

The bass part is just a simple walking bassline with little variation.
The piano plays the current chord using a random inversion (weighted
in favour of the root inversion) and random note length and rests
(weighted to rest more on the beat to syncopate off the bassline).
There is also a special function for each instrument to do a random
closing riff at the end of the song; this is just a random rhythm that
is increasingly likely to hold the note for longer.

TODO
====

- Swing Beat set automatically without having to add it in musescore
  (also, make piano dynamic piano)
- Make duration more likely to be odd if we are already off-beat to
  even it up
- Drum kit (start with hihat at least)
- More varied bassline - occasional quavers, runs, fills etc
- More varied piano - some passing notes and skeletal chords etc
- Other keys (defaults to C in output but roman notation used in code)
- Improve performance, don't do unnecessary stuff with music21 objects
