
::::::::::::::::::::::::::::::::::::
autobebop - A chord/melody generator
::::::::::::::::::::::::::::::::::::

Dylan Leigh August 2018

Generates a pseudorandom chord progression and a melody to go with it.
By default it outputs it in MusicXML.

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

Command line options are not stable yet, see the code. By default, a
song will be dumped to STDIN, so it is easiest to redirect and then
use Musescore or similar to open it::

   python autobebop.py > song.mxl && musescore song.mxl


Algorithm
=========

(This may change as improvements are made)

Autobebop puts a tonic chord at the start and end and then works
backwards from the end, making a weighted random choice between chords
that tend to resolve to the "current" chord. For example::

   I                       I
   I                 V     I
   I           ii    V     I
   I     vi    ii    V     I

The individual notes of the melody are then chosen in a similarly
random fashion favouring notes that are part of the current chord.
Notes part of the current chord are also more likely to be given a
longer duration.

