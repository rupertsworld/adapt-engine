import math
from adapt import Note, Group, get_chord, Scales
from ..tracks.dune import dune

def Dune(sess, key="C4"):
    duration_beats = 8
    if (sess.params["excitement"] > 0.7): duration_beats = 4
    dur = sess.clock.beats(duration_beats)
    chords = [1, 4]
    index = math.floor(sess.clock.to_beats(sess.clock.now()) % (duration_beats * len(chords)) / duration_beats)
    n = round(sess.params["excitement"] * 3)
    interval = chords[index]
    chord = get_chord(key, Scales.MAJOR, interval, n=n)
    notes = [Note(track=dune, value=note, velocity=127, duration=dur) for note in chord]
    if sess.clock.on_beats(duration_beats):
        return Group(*notes)