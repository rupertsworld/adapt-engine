from adapt import Group, Scales, use_random
from app.components.random_chords import RandomChords
from app.components.random_notes import RandomNotes
from app.tracks.dune import dune
from app.tracks.piano import piano
from app.tracks.autumn_water import autumn_water

def Main(sess):
    if not "excitement" in sess.params: sess.params["excitement"] = 0.5
    
    if sess.params["excitement"] < 0.6:
        chord_track = autumn_water
        melody_track = piano
    else:
        chord_track = dune
        melody_track = autumn_water

    return Group(
        RandomChords(
            sess,
            track=chord_track,
            root="C#4",
            scale=Scales.MAJOR
        ),
        RandomNotes(sess, track=melody_track, root="C#5", scale=Scales.PENTATONIC)
    )