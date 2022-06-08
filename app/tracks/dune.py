from app.settings import *
from adapt import VST

class Dune(VST):
    sample_path = SAMPLE_PATH
    durations = [1, 2, 3, 4, 5, 6, 7, 8]
    vst_path = "/Library/Audio/Plug-Ins/VST3/DUNE3.vst3"
    # preset = "my_preset"

dune = Dune()