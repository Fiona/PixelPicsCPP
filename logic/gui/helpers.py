"""
PixelPics - Nonogram game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""


from itertools import izip


def lerp(i, speed, start, end, smooth = True):
    speed -= 1
    p = 1.0/speed*i
    if smooth:
        p = ((p) * (p) * (3 - 2 * (p)))
    return start + (end - start) * p


def reverse_enumerate(l):
    return izip(xrange(len(l)-1, -1, -1), reversed(l))
