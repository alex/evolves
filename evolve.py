#!/usr/bin/env python

import pyglet
from pyglet import gl

IMAGE_FILE_NAME = 'mona_lisa_crop.jpg'

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

class Polygon(object):
    def __init__(self, vertices, color):
        # should be a list of 2 tuples
        self.vertices = vertices
        self.color = color
    
    def draw(self, offset=(0, 0)):
        w, h = offset
        r, g, b, a = self.color
        pyglet.graphics.draw(len(self.vertices), gl.GL_POLYGON,
            ('v2f', [int(p) for p in flatten((x+w, y+h) for x, y in self.vertices)]),
            ('c4B', [int(c) for c in ((r, g, b, a*255) * len(self.vertices))]),
        )
        gl.glColor4f(1, 1, 1, 1)

class Approximater(object):
    def __init__(self, orig):
        self.orig = orig
        self.polys = []
        img = self.orig.get_image_data()
        self.orig_data = partition([ord(x) for x in img.get_data("RGB", img.width*3)], 3)
    
    def append(self, poly):
        self.polys.append(poly)
    
    def fitness(self):
        approx = get_pixel_data(self.orig.width, 0, self.orig.width, self.orig.height)
        diff = 0.0
        for (r1,g1,b1), (r2, g2, b2) in zip(self.orig_data, approx):
        	r_diff = r1 - r2
        	g_diff = g1 - g2
        	b_diff = b1 - b2
        	diff += r_diff**2 + g_diff**2 + b_diff**2
        return diff
    
    def draw(self, offset=(0, 0)):
        for poly in self.polys:
            poly.draw(offset)

class Evolves(pyglet.window.Window):
    def __init__(self):
        super(Evolves, self).__init__(caption="Evolves 2008", 
            width=100, height=100)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        
        self.setup()
    
    def setup(self):
        self.f = pyglet.image.load(IMAGE_FILE_NAME)
        self.set_size(self.f.width*2, self.f.height)
        
        self.approx = Approximater(self.f)
        self.approx.append(Polygon(
            [(0, 0), (0, self.f.height), (self.f.width, self.f.height), (self.f.width, 0)],
            (255, 3, 45, .75)
        ))
        self.approx.append(Polygon(
            [(-25, 10), (-25, 90), (90, 90), (90, 10)],
            (3, 255, 45, .75)
        ))
            
    def on_draw(self):
        self.clear()
        self.f.blit(0, 0)
        self.approx.draw((self.f.width, 0))
        print self.approx.fitness()
    
    def run(self):
        pyglet.app.run()

if __name__ == '__main__':
    Evolves().run()
