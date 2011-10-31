
import gtk

class DemoApp(object):
        
    def build_ui(self):
        window = gtk.Window()
        window.set_default_size(800, 600)
        window.set_title("PyGtkWebWidget - " + self.get_title())
        window.connect("destroy", gtk.main_quit)
        box = gtk.VBox(homogeneous=False, spacing=0)
        box.pack_start(self.get_content(), expand=True, fill=True, padding=0)
        window.add(box)
        self._window = window
        
    def get_title(self):
        pass
    
    def get_content(self):
        pass
    
    def run(self):
        self._window.show_all()
        gtk.main()
