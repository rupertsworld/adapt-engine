from adapt.settings import *
from scipy.io import wavfile
from adapt.mixer import Mixer
from adapt.clock import Clock
# from adapt.vst import bounce
from adapt.events import EventQueue

class Session:
    def __init__(self, component, params={}):
        self.clock = Clock(0, bpm=50, beats_per_bar=4)
        self.component = component
        self.params = params
        self.event_queue = EventQueue()
        self.mixer = Mixer()
        self.hooks = []
        self.current_hook = 0

    def update_params(self, params):
        self.params = params
    
    def get_events(self):
        event = self.component(sess=self)
        return event
    
    def reset_events(self):
        self.mixer.reset_events()
        self.event_queue = EventQueue()
    
    def use_state(self, init_value):
        if len(self.hooks) <= self.current_hook:
            self.hooks.append(init_value)
        
        hook_index = self.current_hook

        def state():
            return self.hooks[hook_index]
        
        def set_state(new_state):
            self.hooks[hook_index] = new_state
        
        self.current_hook += 1
        return state, set_state
    
    def render(self, duration_secs):
        duration = self.clock.secs(duration_secs)
        render_start = self.clock.now()

        # Generate events
        while self.clock.ticks <= render_start + duration:
            event = self.get_events()

            if not event:
                self.clock.tick()
                continue
            
            event.set_offset(self.clock.now() - render_start)
            event.set_clock(self.clock)
            self.event_queue.add(event)
            self.clock.tick()

        # Generate audio from events
        for track, events in self.event_queue:
            self.mixer.add(track, events)
        
        audio = self.mixer.bounce(duration_secs)

        self.reset_events()
        return audio
        
    def render_to_file(self, path, duration_secs):
        audio = self.render(duration_secs)
        wavfile.write(path, SAMPLE_RATE, audio)