
::::::::::::::::::::::::::::::::::::
autobebop - A chord/melody generator
::::::::::::::::::::::::::::::::::::

TODO: Rename - AutoJazzComp ? PseudoRandomRhythmSection

Dylan Leigh August 2018

Generates a pseudorandom chord progression and a melody to go with it,
outputs a score in MusicXML.

Installation/Requirements
=========================

Other than Python the only hard requirement is the Music21 library
[http://web.mit.edu/music21/] which is used for writing the MusicXML.

A pip requirements file is provided, and it is recommended that
Virtualenv or a similar system be used for a clean environment::

   virtualenv autobebop
   cd autobebop
   . bin/activate
   git clone http://git/TODO
   pip install -r requirements.txt

Usage
=====

**Command line options are not stable yet, see the code. Sorry.**

By default, the song will be saved in /tmp/ and the name will be
printed to standard output, so it can be easily opened with
Musescore or other MusicXML software::

   $ python autobebop.py
   /tmp/music21/tmpF1MSXf.xml
   $ musescore /tmp/music21/tmpF1MSXf.xm

Or::
   $ musescore `python autobebop.py`


Algorithm
=========

(This may change as improvements are made)

Autobebop puts a tonic chord at either end and then works backwards,
making a weighted random choice between chords that tend to resolve to
the "current" chord. For example::

   I                       I
   I                 V     I
   I           ii    V     I
   I     vi    ii    V     I

The individual notes of the melody are then chosen in a similarly
random fashion favouring notes that are part of the current chord.
Notes part of the current chord are also more likely to be given a
longer duration.

TODO
====

- Piano Chords working
- Alto notes (quavers) working
- Varied note durations
- Rests
- Swing Beat
- Piano does some comping rhythm
- Other keys (defaults to C)
- Include chord symbols in the score
- Chord inversions in the comp
