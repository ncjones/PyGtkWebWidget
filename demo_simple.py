#!/usr/bin/env python

# Copyright 2011 Nathan Jones
#
# This file is part of PyGtkWebWidget.
#
# PyGtkWebWidget is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# PyGtkWebWidget is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyGtkWebWidget.  If not, see <http://www.gnu.org/licenses/>.

import gtk
import os
import gtkweb
import datetime

window = gtk.Window()
window.connect("destroy", gtk.main_quit)
box = gtk.VBox(homogeneous=False, spacing=0)
window.add(box)
demo_uri = "file://" + os.path.abspath('demo_simple.html')
web_widget = gtkweb.WebWidget(demo_uri)
box.pack_start(web_widget, expand=True, fill=True, padding=0)
window.set_default_size(800, 600)
window.show_all()
def on_click(timestamp):
	global web_widget
	print "clicked: ", datetime.datetime.fromtimestamp(float(timestamp)/1000)
	print "click count: " , web_widget.invoke("getClickCount")
web_widget.subscribe("click", on_click)
gtk.main()
