#!/usr/bin/env python

import pyglet
from pyglet import gl

IMAGE_FILE_NAME = 'mona_lisa_crop.jpg'

def flatten(seq):
    if not hasattr(seq, '__iter__'):
        yield seq
    else:
        for item in seq:
            for i in flatten(item):
                yield i

class Polygon(object):
    def __init__(self, vertices, color):
        # should be a list of 2 tuples
        self.vertices = vertices
        self.color = color
    
    def draw(self, offset=(0, 0)):
        w, h = offset
        pyglet.graphics.draw(len(self.vertices), gl.GL_POLYGON,
                ('v2f', [int(p) for p in flatten((x+w, y+h) for x, y in self.vertices)]),
                ('c4B', self.color * len(self.vertices)),
            )
        gl.glColor4f(1, 1, 1, 1)

class Approximater(object):
    def __init__(self, orig):
        self.orig = orig
        self.polys = []
    
    def append(self, poly):
        self.polys.append(poly)
    
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
            (255, 3, 45, 125)
        ))
            
    def on_draw(self):
        self.clear()
        self.f.blit(0, 0)
        self.approx.draw((self.f.width, 0))
    
    def run(self):
        pyglet.app.run()

if __name__ == '__main__':
    Evolves().run()
