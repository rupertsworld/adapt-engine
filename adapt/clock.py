ticks_per_beat = 48

class Clock:
    def __init__(self, init_ticks=0, bpm=120, beats_per_bar=4):
        self.ticks = init_ticks
        self.bpm = bpm
        self.beats_per_bar = beats_per_bar
        self.ticks_per_bar = ticks_per_beat * beats_per_bar
    
    def now(self):
        return self.ticks
    
    def tick(self):
        self.ticks += 1

    def on_bars(self, n, offset=0):
        return not (self.ticks + self.ticks_per_bar * offset) % (self.ticks_per_bar * n)
    
    def on_beats(self, n, offset=0):
        return not (self.ticks + ticks_per_beat * offset) % (ticks_per_beat * n)
    
    def to_secs(self, ticks):
        beats_per_second = self.bpm / 60
        ticks_per_second = ticks_per_beat * beats_per_second
        secs = ticks / ticks_per_second
        return secs

    def to_beats(self, ticks):
        return ticks / ticks_per_beat

    def secs(self, secs):
        beats_per_second = self.bpm / 60
        ticks_per_second = ticks_per_beat * beats_per_second
        ticks = secs * ticks_per_second
        return ticks

    def beats(self, n):
        return ticks_per_beat * n
    
    def bars(self, n):
        return self.ticks_per_bar * n