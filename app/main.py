from adapt import Group, Scales, bracket
from adapt import Scales
from app.components.piano_flourish import PianoFlourish
from .components.dune import Dune

def Main(clock, params):
    if not "excitement" in params:
        params["excitement"] = 0.5

    return Group(
        Dune(clock, params, key="F4"),
        PianoFlourish(clock, params, key="F", octave=5, scale=Scales.PENTATONIC)
    )