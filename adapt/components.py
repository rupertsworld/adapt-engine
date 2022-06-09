from helpers import bracket
from numpy.random import normal

# def Progression(*children, every_bars=12):
#     num_children = len(children)
    
#     bracket_obj = {}
#     for i in range(0, num_children):
#         bracket_obj[every_bars]

#     brackets = bracket({0})


def RandomProgression(clock, params, every_bars=12, deviation_bars=6, *children):
    num_children = len(children)
    next_break = round(normal(every_bars, deviation_bars))
