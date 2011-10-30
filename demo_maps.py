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

marker_list_store = gtk.ListStore(float, float)
marker_tree_view = gtk.TreeView(marker_list_store)
latitude_column = gtk.TreeViewColumn("Latitude")
latitude_cell = gtk.CellRendererText()
latitude_column.pack_start(latitude_cell)
latitude_column.add_attribute(latitude_cell, "text", 0)
longitude_column = gtk.TreeViewColumn("Longitude")
longitude_cell = gtk.CellRendererText()
longitude_column.pack_start(longitude_cell)
longitude_column.add_attribute(longitude_cell, "text", 1)
marker_tree_view.append_column(latitude_column)
marker_tree_view.append_column(longitude_column)

window = gtk.Window()
window.connect("destroy", gtk.main_quit)
box = gtk.HBox(homogeneous=False, spacing=0)
window.add(box)

demo_uri = "file://" + os.path.abspath("demo_maps.html")
web_widget = gtkweb.WebWidget(demo_uri)
def on_marker_added(marker):
    index = marker["index"]
    latitude = marker["lat"]
    longitude = marker["lng"]
    marker_list_store.insert(index, [latitude, longitude])
def on_marker_selection_changed(index):
    iter = marker_list_store.get_iter(index)
    marker_tree_view.get_selection().select_iter(iter)
web_widget.subscribe("marker-added", on_marker_added)
web_widget.subscribe("selection-changed", on_marker_selection_changed)

def on_marker_tree_selection_changed(selection):
    iter = selection.get_selected()[1]
    path = marker_list_store.get_path(iter)
    web_widget.invoke("selectMarker", path[0])
marker_tree_view.get_selection().connect("changed", on_marker_tree_selection_changed)

box.pack_start(web_widget, expand=True, fill=True, padding=0)
box.pack_end(marker_tree_view)
window.set_default_size(800, 600)
window.show_all()
gtk.main()

