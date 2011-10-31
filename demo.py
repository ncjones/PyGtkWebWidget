
import gtk

class DemoApp(object):
        
    def build_ui(self):
        window = gtk.Window()
        window.set_default_size(800, 600)
        window.set_title("PyGtkWebWidget - " + self.get_title())
        window.connect("destroy", gtk.main_quit)
        box = gtk.VBox(homogeneous=False, spacing=0)
        box.pack_start(self.get_header(), expand=False, fill=False, padding=0)
        box.pack_start(self.get_content(), expand=True, fill=True, padding=0)
        window.add(box)
        self._window = window
        
    def get_title(self):
        pass
    
    def get_description(self):
        pass
    
    def get_header(self):
        label = gtk.Label(self.get_description())
        label.set_use_markup(True)
        label.set_selectable(True)
        label.set_can_focus(False)
        label.set_line_wrap_mode(True)
        label.set_alignment(0, 0)
        label.set_padding(10, 10)
        return label
    
    def get_content(self):
        pass
    
    def run(self):
        self._window.show_all()
        gtk.main()
