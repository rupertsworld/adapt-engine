from pydub import AudioSegment
import numpy as np

class Scales:
    MAJOR = (2, 2, 1, 2, 2, 2, 1)
    PENTATONIC = (2, 2, 3, 2, 3)


def midi(note):
    initial_notes = {
        "C": 0,
        "C#": 1,
        "D": 2,
        "D#": 3,
        "E": 4,
        "F": 5,
        "F#": 6,
        "G": 7,
        "G#": 8,
        "A": 9,
        "A#": 10,
        "B": 11
    }
    
    octave = 0
    note_name = "C"
    if '#' in note:
        components = note.split('#')
        note_name = components[0] + '#'
        octave = int(components[1])
    else:
        note_name = note[0]
        octave = int(note[1])

    note_name = note_name.upper()
    if note_name in initial_notes.keys():
        return initial_notes[note_name] + octave * 12
    else:
        raise IndexError(f"Note name '{note_name}' is not valid.")


def get_scale(note="C", signature=Scales.MAJOR, min_midi=33, max_midi=105):
    if min_midi < 0:
        raise IndexError(f"Start note '{min_midi}' is below minimum MIDI note.")
    if max_midi > 127:
        raise IndexError(f"Start note '{max_midi}' is above maximum MIDI note.")
    if max_midi <= min_midi:
        raise IndexError(
            f"Minimum MIDI note '{min_midi}' is greater than the maximum '{max_midi}'."
        )


    start_note_midi = midi(note)
    while start_note_midi < min_midi:
        start_note_midi += 12

    scale = []
    current_note = start_note_midi
    scale_index = 0 # 1st note out of 7 in a scale
    sig_list = signature

    while current_note < max_midi:
        scale.append(current_note)
        current_note += sig_list[scale_index % len(sig_list)] # Loop if at the octave
        scale_index += 1

    return scale


def accum(lis):
    total = 0
    for x in lis:
        total += x
    return total

def get_chord(root="C4", signature=Scales.MAJOR, interval=1, n=3):
    interval = (interval - 1) % 8 
    scale = []
    key_midi = midi(root)
    signature = [*signature, *signature]

    scale.append(key_midi + accum(signature[:interval]))
    if n > 1: scale.append(scale[0] + accum(signature[interval:interval + 2]))
    if n > 2: scale.append(scale[1] + accum(signature[interval + 2:interval + 4]))

    return scale


# def ticks_to_seconds(ticks, bpm):
#         beats_per_second = bpm / 60
#         ticks_per_second = ticks_per_beat * beats_per_second
#         seconds = ticks / ticks_per_second
#         return seconds


def beats_to_seconds(beats, bpm):
        beats_per_second = bpm / 60
        seconds = beats / beats_per_second
        return seconds
    
def bracket(brackets, repeat_after=None):
    def fn(value):
        if repeat_after: value = value % repeat_after

        for maximum in sorted(list(brackets.keys())):
            if value < maximum:
                return brackets[maximum]

        return list(brackets.values())[-1]
    return fn