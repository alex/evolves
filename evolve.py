import gobject
import gtk
import gtk.glade
import pygtk

class Evolves(object):
    def __init__(self):
        self.gladefile = 'ui.glade'
        self.wTree = gtk.glade.XML(self.gladefile, 'main_window')
        self.wTree.signal_autoconnect(self)
        
    def quit(self, *args, **kwargs):
        gtk.main_quit()
    
    def run(self):
        gtk.main()

if __name__ == '__main__':
    Evolves().run()
