from pyglet import gl

def partition(seq, chunk_size):
    return [seq[i:i+chunk_size] for i in xrange(0, len(seq), chunk_size)]

def flatten(seq):
    if not hasattr(seq, '__iter__'):
        yield seq
    else:
        for item in seq:
            for i in flatten(item):
                yield i

def get_pixel_data(x, y, width, height):
    p = (4*width*height*gl.GLubyte)()
    gl.glReadPixels(x, y, width, height, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, p)
    return [(r, g, b) for r, g, b, a in partition(p, 4)]

class Dummy(object):
    pass
