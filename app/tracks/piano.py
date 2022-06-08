from app.settings import *
from adapt import VST

class Piano(VST):
    sample_path = SAMPLE_PATH
    vst_path = "/Library/Audio/Plug-Ins/VST/LABS.vst"

piano = Piano()