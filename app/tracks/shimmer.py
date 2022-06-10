from app.settings import *
from adapt import VST

# Dune3 – Animated Shimmer

class Shimmer(VST):
    sample_path = SAMPLE_PATH
    durations = [1, 2, 3, 4, 5, 6, 7, 8, 12, 15, 20]
    vst_path = "/Library/Audio/Plug-Ins/VST3/DUNE3.vst3"

shimmer = Shimmer()