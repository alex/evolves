#!/usr/bin/env python

import pyglet

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
        pyglet.graphics.draw(len(self.vertices), pyglet.gl.GL_POLYGON,
                ('v2i', [int(p) for p in flatten((x+w, y+h) for x, y in self.vertices)]),
                ('c4b', self.color * len(self.vertices)),
            )

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
        self.f = pyglet.image.load(IMAGE_FILE_NAME)
        super(Evolves, self).__init__(caption="Evolves 2008", 
            width=self.f.width*2, height=self.f.height)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    
    def on_draw(self):
        self.clear()
        self.f.blit(0, 0)
        x = Approximater(None)
        x.append(Polygon(
            [(0, 0), (self.f.width, 0), (self.f.width, self.f.height), (0, self.f.height)],
            (255, 3, 45, 100)
        ))
        x.draw((self.f.width, 0))
    
    def run(self):
        pyglet.app.run()

if __name__ == '__main__':
    Evolves().run()
