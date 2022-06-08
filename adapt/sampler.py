from adapt.settings import *
from adapt.track import Track
from scipy.io import wavfile
import numpy as np
import math, os

buffer_size = 128

# Maximum sample length = NOTE_RENDER_DURATION_SECS
class Sampler(Track):
    sample_path = ""
    samples = {}

    def __init__(self):
        super().__init__()
        if 'ADAPT_SAMPLE_PATH' in os.environ:
            self.sample_path = os.path.abspath(os.environ['ADAPT_SAMPLE_PATH'])
        self.sample_path = f"{self.sample_path}/{self.name}"
        for key, value in self.samples.items():
            self.samples[key] = f"{self.sample_path}/{value}"

    def bounce(self, events, render_length_secs):
        render_length_secs += NOTE_RENDER_DURATION_SECS
        duration_samples = math.ceil(SAMPLE_RATE * render_length_secs)
        final_audio = np.zeros((duration_samples, 2), dtype=np.int16)

        for event in events:
            base_audio = np.zeros((duration_samples, 2), dtype=np.int16)
            sample_path = self.samples[event.value]
            _, sample = wavfile.read(sample_path)
            insert_at = int(event.offset_secs * SAMPLE_RATE)
            base_audio = np.insert(base_audio, insert_at, sample, axis=0)
            final_audio += base_audio[:duration_samples]
        
        return final_audio
