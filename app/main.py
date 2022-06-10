from adapt import Group, Scales, use_random
from app.components.piano_flourish import PianoFlourish
from .components.dune import Dune

def Main(sess):
    if not "excitement" in sess.params:
        sess.params["excitement"] = 0.5
    
    section = use_random(['intro', 'solo'], sess=sess, every_bars=2)

    if section == 'intro':
        return PianoFlourish(sess, key="F", octave=5, scale=Scales.PENTATONIC)
    elif section == 'solo':
        return Dune(sess, key="F4")