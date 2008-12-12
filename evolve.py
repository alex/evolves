import gobject
import gtk
import gtk.glade
import pygtk

IMAGE_FILE_NAME = 'mona_lisa_crop.jpg'

class Evolves(object):
    def __init__(self):
        self.gladefile = 'ui.glade'
        self.wTree = gtk.glade.XML(self.gladefile, 'main_window')
        self.wTree.signal_autoconnect(self)
        
        self.setup_widgets()
        
        img = gtk.gdk.pixbuf_new_from_file(IMAGE_FILE_NAME)
        self.original.window.draw_pixbuf(None, img, 0, 0, 0, 0)
    
    def setup_widgets(self):
        self.original = self.wTree.get_widget('real_image')
        self.best = self.wTree.get_widget('best')
        self.evolves = self.wTree.get_widget('evolves')
    
    def quit(self, *args, **kwargs):
        gtk.main_quit()
    
    def run(self):
        gtk.main()

if __name__ == '__main__':
    Evolves().run()
