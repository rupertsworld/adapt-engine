from app.settings import *
from adapt import VST

# Dune3 – Airy Voice Pad RL

class AiryVoice(VST):
    sample_path = SAMPLE_PATH
    durations = [2, 3, 4, 5, 6, 7, 8, 12, 15, 20]
    vst_path = "/Library/Audio/Plug-Ins/VST3/DUNE3.vst3"

airy_voice = AiryVoice()