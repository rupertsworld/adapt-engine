from .clock import Clock

class Event:
    def __init__(self):
        self.offset_secs = 0
        self.clock = None
    
    def set_offset(self, offset):
        self.offset = offset
        if self.clock: self.offset_secs = self.clock.to_secs(offset)

    def set_clock(self, clock):
        self.clock = clock
        if hasattr(self, "offset"): self.offset_secs = clock.to_secs(self.offset)


class Group(Event):
    def __init__(self, *events):
        super().__init__()
        self.events = events

    def expand(self):
        expanded_events = []

        for event in self.events:
            if not event: continue

            event.set_clock(self.clock)
            event.set_offset(self.offset)
            
            for e in event.expand():
                e.set_offset(self.offset)
                e.set_clock(self.clock)
                expanded_events.append(e)
        
        return expanded_events


class RootEvent(Event):
    def expand(self):
        return [self]


class Note(RootEvent):
    def __init__(self, track, value, velocity, duration):
        super().__init__()
        self.track = track
        self.value = value
        self.velocity = velocity
        self.duration = duration
    
    def set_clock(self, clock):
        super().set_clock(clock)
        if hasattr(self, 'duration'): self.duration_secs = clock.to_secs(self.duration)


class Sample(RootEvent):
    def __init__(self, track, value):
        super().__init__()
        self.track = track
        self.value = value


class EventQueue:
    def __init__(self):
        self.events_by_track = {}

    def __iter__(self):
        self.n = 0
        return self
    
    def __next__(self):
        keys = list(self.events_by_track.keys())
        if self.n < len(keys):
            track_events = self.events_by_track[keys[self.n]]
            track = track_events["track"]
            events = track_events["events"]
            self.n += 1
            return track, events
        else:
            raise StopIteration

    def add(self, event):
        events = event.expand()

        # These are all RootEvents
        for event in events:
            track_name = event.track.name
            if not track_name in self.events_by_track:
                self.events_by_track[track_name] = {
                    "track": event.track,
                    "events": []
                }
            self.events_by_track[track_name]["events"].append(event)