from adapt.settings import *
import numpy as np
import math

tail_length_samples = math.ceil(SAMPLE_RATE * NOTE_RENDER_DURATION_SECS)

class Mixer:
    def __init__(self):
        self.tracks_events = []
        self.tail = np.zeros((tail_length_samples, 2), dtype=np.int16)
    
    def add(self, track, events):
        self.tracks_events.append({
            "track": track,
            "events": events
        })
    
    def reset_events(self):
        self.tracks_events = []

    def bounce(self, duration_secs):
        track_audio = []
        duration_samples = math.ceil(SAMPLE_RATE * duration_secs)

        if not self.tracks_events:
            track_audio.append(np.zeros((duration_samples, 2), dtype=np.int16))
        
        mixed_audio = np.zeros((duration_samples, 2), dtype=np.int16)

        # Add the tail
        if tail_length_samples <= duration_samples:
            long_tail = np.zeros((duration_samples, 2), np.int16)
            long_tail = np.insert(long_tail, 0, self.tail, axis=0)
            mixed_audio += long_tail[:duration_samples]
        else:
            mixed_audio += self.tail[:duration_samples]

        # Cut off the added parts of the tail
        new_tail = np.zeros((tail_length_samples, 2), np.int16)
        new_tail = np.insert(new_tail, 0, self.tail[duration_samples:], axis=0)
        new_tail = new_tail[:tail_length_samples]
        self.tail = new_tail

        for item in self.tracks_events:
            audio = item["track"].bounce(item["events"], duration_secs)
            track_audio.append(audio[:duration_samples])
            tail = np.zeros((tail_length_samples, 2), np.int16)
            tail = np.insert(tail, 0, audio[duration_samples:], axis=0)
            tail = tail[:tail_length_samples]
            self.tail += tail
        
        for audio in track_audio: mixed_audio += audio
        
        return mixed_audio
        

