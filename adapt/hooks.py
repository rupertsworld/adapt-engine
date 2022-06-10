from random import randint

def use_random(options, sess, every_ticks=96, deviation_ticks=48):
    def get_break():
        return sess.clock.now() + every_ticks # sess.clock.bars(round(normal(every_bars, deviation_bars)))
    
    def get_random_index():
        return randint(0, len(options) - 1)

    next_break, set_next_break = sess.use_state(get_break())
    index, set_index = sess.use_state(get_random_index())

    if sess.clock.now() >= next_break():
        set_index(get_random_index())
        set_next_break(get_break())

    return options[index()]