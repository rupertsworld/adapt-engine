from adapt import Chord, use_random

def RandomChords(sess, track, root, scale):
    every_ticks = sess.clock.bars(2)
    note_num = use_random([1, 2, 3, 4, 5, 6, 7], sess=sess, every_ticks=every_ticks)

    if sess.clock.on_ticks(every_ticks):
        return Chord(
            sess,
            track=track,
            root=root,
            scale=scale,
            note_num=note_num,
            duration_ticks=every_ticks
        )
