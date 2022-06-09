from adapt import Group, Scales, bracket
from adapt import Scales
from app.components.piano_flourish import PianoFlourish
from .components.dune import Dune

def Main(sess):
    if not "excitement" in sess.params:
        sess.params["excitement"] = 0.5

    return Group(
        Dune(sess, key="F4"),
        PianoFlourish(sess, key="F", octave=5, scale=Scales.PENTATONIC)
    )