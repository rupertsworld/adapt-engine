import math
from adapt import Note, Group, get_chord, Scales
from ..tracks.dune import dune

# start = 1
def Dune(clock, params, key="C4"):
    # global start
    duration_beats = 8
    if (params["excitement"] > 0.7): duration_beats = 4
    dur = clock.beats(duration_beats)
    chords = [1, 4]
    index = math.floor(clock.to_beats(clock.now()) % (duration_beats * len(chords)) / duration_beats)
    n = round(params["excitement"] * 3)
    interval = chords[index]
    chord = get_chord(key, Scales.MAJOR, interval, n=n)
    notes = [Note(track=dune, value=note, velocity=127, duration=dur) for note in chord]
    if clock.on_beats(duration_beats):
        return Group(*notes)