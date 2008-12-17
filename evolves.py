#!/usr/bin/env python

from random import choice, randrange, random

import pyglet
from pyglet import gl

from constants import IMAGE_FILE_NAME, INITIAL_POLYGONS, INITIAL_VERTICES_PER_POLYGON
from utils import partition, flatten, get_pixel_data, Dummy

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
    
    def clone(self):
        obj = Dummy()
        obj.__class__ = self.__class__
        obj.vertices = self.vertices[:]
        obj.color = self.color
        return obj

class PolygonSet(object):
    def __init__(self, polys, start, size, orig):
        self.polys = polys
        self.start = start
        self.size = size
        self.orig = orig
    
    def clone(self, **extra):
        obj = Dummy()
        obj.__class__ = self.__class__
        obj.polys = [x.clone() for x in self.polys]
        obj.start = self.start
        obj.size = self.size
        obj.orig = self.orig
        obj.__dict__.update(extra)
        return obj
    
    def mutate(self):
        p = choice(self.polys)
        if random() > .5:
            p.vertices[randrange(0, len(p.vertices))] = (randrange(0, self.size[0]), randrange(0, self.size[1]))
        else:
            c = random()
            if c < .25:
                p.color = (randrange(0, 255), p.color[1], p.color[2], p.color[3])
            elif c < .5:
                p.color = (p.color[0], randrange(0, 255), p.color[2], p.color[3])
            elif c < .75:
                p.color = (p.color[0], p.color[1], randrange(0, 255), p.color[3])
            else:
                p.color = (p.color[0], p.color[1], p.color[2], random())
    
    def append(self, poly):
        self.polys.append(poly)
    
    def fitness(self):
        approx = get_pixel_data(self.start[0], self.start[1], self.size[0], self.size[1])
        diff = 0.0
        for (r1,g1,b1), (r2, g2, b2) in zip(self.orig, approx):
        	r_diff = r1 - r2
        	g_diff = g1 - g2
        	b_diff = b1 - b2
        	diff += r_diff**2 + g_diff**2 + b_diff**2
        return diff
    
    def draw(self):
        for poly in self.polys:
            poly.draw(self.start)

class Approximater(object):
    def __init__(self, orig):
        self.orig = orig
        img = self.orig.get_image_data()
        self.orig_data = partition([ord(x) for x in img.get_data("RGB", img.width*3)], 3)
        
        self.setup()
        
        self.evolutions = 0
        self.bene_evolutions = 0
        
    def setup(self):
        self.best = PolygonSet([], (self.orig.width, 0), (self.orig.width, self.orig.height), self.orig_data)
        self.current_approx = PolygonSet([], (self.orig.width*2, 0), (self.orig.width, self.orig.height), self.orig_data)

        for i in xrange(INITIAL_POLYGONS):
            self.current_approx.append(Polygon(
                [(randrange(0, self.orig.width), randrange(0, self.orig.height)) for j in xrange(INITIAL_VERTICES_PER_POLYGON)],
                (randrange(0, 255), randrange(0, 255), randrange(0, 255), random())
            ))
    
    def evolve(self, *args, **kwargs):
        self.current_approx.mutate()
        self.evolutions += 1
        self.current_approx.draw()
        if self.current_approx.fitness() >= self.best.fitness():
            self.best = self.current_approx.clone(start=self.best.start)
            self.best.draw()
            self.bene_evolutions += 1
        else:
            self.current_approx = self.best.clone(start=self.current_approx.start)
            self.current_approx.draw()
        print "%s / %s" % (self.bene_evolutions, self.evolutions)
    
    def draw(self):
        self.current_approx.draw()
        self.best.draw()

class Evolves(pyglet.window.Window):
    def __init__(self):
        super(Evolves, self).__init__(caption="Evolves 2008", 
            width=100, height=100)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        
        self.setup()
    
    def setup(self):
        self.f = pyglet.image.load(IMAGE_FILE_NAME)
        self.set_size(self.f.width*3, self.f.height)
        
        self.approx = Approximater(self.f)
        
        pyglet.clock.schedule(self.approx.evolve)
        
    def on_draw(self):
        self.clear()
        self.f.blit(0, 0)
        self.approx.draw()
    
    def run(self):
        pyglet.app.run()

if __name__ == '__main__':
    Evolves().run()
