from .events import Group, Note
from .helpers import Scales, get_chord

def Chord(sess, track, root="C4", scale=Scales.MAJOR, note_num=0, duration_ticks=96, velocity=127):
    chord = get_chord(root, scale, note_num)
    
    notes = []
    for note in chord:
        note = Note(track=track, value=note, velocity=velocity, duration=duration_ticks)
        notes.append(note)
    
    return Group(*notes)