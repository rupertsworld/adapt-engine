from adapt import Group, Scales, use_random
from app.components.random_chords import RandomChords
from app.components.random_notes import RandomNotes
from app.tracks.dune import dune
from app.tracks.piano import piano
from app.tracks.autumn_water import autumn_water

def Main(sess):
    if not "excitement" in sess.params:
        sess.params["excitement"] = 0.5
    
    # section = use_random(['breakdown', 'full'], sess=sess, every_ticks=sess.clock.bars(6))
    
    if sess.params["excitement"] < 0.6:
        return Group(
                RandomChords(
                sess,
                track=autumn_water,
                root="C#4",
                scale=Scales.MAJOR
            ),
            RandomNotes(sess, piano, key="C#", octave=5, scale=Scales.PENTATONIC)
        )
    else:
        return Group(
            RandomChords(
                sess,
                track=dune,
                root="C#4",
                scale=Scales.MAJOR
            ),
            RandomNotes(sess, autumn_water, key="C#", octave=5, scale=Scales.PENTATONIC)
        )
        
        
    # section = use_random(['intro', 'solo'], sess=sess, every_bars=2)

    # if section == 'intro':
    #     return PianoFlourish(sess, key="F", octave=5, scale=Scales.PENTATONIC)
    # elif section == 'solo':
    #     return Dune(sess, key="F4")