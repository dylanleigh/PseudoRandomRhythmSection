
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
PseudoRandomRhythmSection - Generate a random swing progression & comp
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

Dylan Leigh - August 2018

Generates a pseudorandom chord progression and piano/bass comp to go
with it, outputs a score in MusicXML.

Installation/Requirements
=========================

Other than Python the only hard requirement is the Music21 library
http://web.mit.edu/music21/ which is used for writing the MusicXML.

A pip requirements file is provided, and it is recommended that
Virtualenv or a similar system be used for a clean environment::

   virtualenv prrs
   cd prrs
   . bin/activate
   git clone http://git/TODO
   pip install -r requirements.txt

Usage
=====

**Command line options are not stable yet, see the code. Sorry.**

By default, the song will be saved in /tmp/ and the name will be
printed to standard output, so it can be easily opened with
Musescore or other MusicXML software::

   $ python prrs.py
   musescore /tmp/music21/tmpF1MSXf.xml
   $ musescore /tmp/music21/tmpF1MSXf.xm

Or::
   $ `python prrs.py`


Algorithm
=========

(This may change as improvements are made)

To generate the chord progression, PRRS puts a tonic chord at either
end and then works backwards, making a weighted random choice between
chords that tend to resolve to the "current" chord. For example::

      I                       I
      I                 V     I
      I           ii    V     I
      I     vi    ii    V     I

Then the actual notes are generated working forwards. First a duration
is chosen for the current chord, then for each instrument a function
is called to generate notes for that duration. Chords that are more
cadentially significant are more likely to have a longer duration.

The bass part is just a simple walking bassline with little variation.
The piano plays the current chord using a random inversion (weighted
towards the root) and random note length and rests (weighted to rest
more on the beat to syncopate off the bassline). There is also a
special function for each instrument to do a random closing riff at
the end of the song.

TODO
====

- CLI options for stuff
- Drum kit (start with hihat at least)
- Swing Beat set (may not be able to do this within music21 :( )
- Include chord symbols in the score (ditto, :( )
- More varied bassline - occasional quavers, runs, fills etc
- More varied piano - some passing notes and skeletal chords etc
- Other keys (defaults to C in output but roman notation used in code)
