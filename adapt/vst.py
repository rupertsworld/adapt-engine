from adapt.settings import *
from adapt.track import Track
from collections import OrderedDict
from bisect import bisect_left
from scipy.io import wavfile
import numpy as np
import math, os

if (not 'ENV' in os.environ) or (os.environ['ENV'] not in ['production', 'container']):
    import dawdreamer

buffer_size = 128

class VST(Track):
    notes = np.arange(21, 109)
    velocities = [127]
    # velocities = np.arange(7, 128, 40)
    durations = np.arange(0.1, 2, 0.3)

    def __init__(self):
        super().__init__()
        if 'ADAPT_PRESAMPLE_PATH' in os.environ:
            self.sample_path = os.path.abspath(os.environ['ADAPT_PRESAMPLE_PATH'])
        self.sample_path = f"{self.sample_path}/{self.name}"
        self.make_samples_dict()

    def preload(self):
        print(f"\n\nPRELOADING SAMPLES FOR: {self.name}\n")

        if not os.path.exists(self.sample_path):
            os.makedirs(self.sample_path)

        engine = dawdreamer.RenderEngine(SAMPLE_RATE, buffer_size)
        vst = engine.make_plugin_processor('my_track', self.vst_path)
        vst.open_editor()
        graph = [(vst, [])]
        engine.load_graph(graph)
 
        for note in self.notes:
            print(f"Generating track={self.name} note={note}")
            for vel in self.velocities:
                for dur in self.durations:
                    filename = self.samples[note][vel][dur]
                    vst.add_midi_note(note, vel, 0, dur)
                    engine.render(NOTE_RENDER_DURATION_SECS)
                    vst.clear_midi()
                    audio = engine.get_audio().transpose()[:, [0, 1]]
                    wavfile.write(filename, SAMPLE_RATE, audio)
                    
    def make_samples_dict(self):
        self.samples = OrderedDict()
        for note in self.notes:
            for vel in self.velocities:
                for dur in self.durations:
                    dur_str = "{:.2f}".format(dur)
                    filename = f"{self.sample_path}/{note}_{vel}_{dur_str}.wav"
                    if not note in self.samples: self.samples[note] = OrderedDict()
                    if not vel in self.samples[note]: self.samples[note][vel] = OrderedDict()
                    self.samples[note][vel][dur] = filename

    def get_nearest_sample(self, event):
        attrs = {
            "note": event.value,
            "vel": event.velocity,
            "dur": event.duration_secs
        }
        
        # Go through each layer of dict and find closest match to key
        value = self.samples
        for attr in attrs.values():
            keys = list(value.keys())
            index = bisect_left(keys, attr)
            key = keys[index - 1] if index in keys else keys[-1]
            value = value[key]

        return value

    def bounce(self, events, render_length_secs):
        # Account for tail of longest note
        render_length_secs += NOTE_RENDER_DURATION_SECS
        duration_samples = math.ceil(SAMPLE_RATE * render_length_secs)
        final_audio = np.zeros((duration_samples, 2), dtype=np.int16)

        for event in events:
            base_audio = np.zeros((duration_samples, 2), dtype=np.int16)
            sample_path = self.get_nearest_sample(event)
            _, sample = wavfile.read(sample_path)
            insert_at = int(event.offset_secs * SAMPLE_RATE)
            base_audio = np.insert(base_audio, insert_at, sample, axis=0)
            final_audio += base_audio[:duration_samples] // 5
        
        return final_audio
