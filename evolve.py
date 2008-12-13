import pyglet


IMAGE_FILE_NAME = 'mona_lisa_crop.jpg'

class Evolves(object):
    def __init__(self):
        pass
    
    def run(self):
        pyglet.app.run()
    

if __name__ == '__main__':
    Evolves().run()
