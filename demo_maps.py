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

import demo
import gtk
import os
import gtkweb
import datetime

class MapDemo(demo.DemoApp):
    
    def __init__(self):
        demo_uri = "file://" + os.path.abspath("demo_maps.html")
        self._web_widget = gtkweb.WebWidget(demo_uri)
        self._web_widget.subscribe("marker-added", self.on_marker_added)
        self._web_widget.subscribe("selection-changed", self.on_marker_selection_changed)
        self._marker_list_store = gtk.ListStore(float, float)
        self._marker_tree_view = self._create_tree_view()
        self._marker_tree_view.get_selection().connect("changed", self.on_marker_tree_selection_changed)
        
    def get_title(self):
        return "Maps Demo"
        
    def get_content(self):
        box = gtk.HBox(homogeneous=False, spacing=0)
        box.pack_start(self._web_widget, expand=True, fill=True, padding=0)
        box.pack_end(self._marker_tree_view)
        return box
        
    def _create_tree_view(self):
        marker_tree_view = gtk.TreeView(self._marker_list_store)
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
        return marker_tree_view

    def on_marker_added(self, marker):
        index = marker["index"]
        latitude = marker["lat"]
        longitude = marker["lng"]
        self._marker_list_store.insert(index, [latitude, longitude])
        
    def on_marker_selection_changed(self, index):
        iter = self._marker_list_store.get_iter(index)
        self._marker_tree_view.get_selection().select_iter(iter)
    
    def on_marker_tree_selection_changed(self, selection):
        iter = selection.get_selected()[1]
        path = self._marker_list_store.get_path(iter)
        self._web_widget.invoke("selectMarker", path[0])

if __name__ == '__main__':
    map_demo = MapDemo()
    map_demo.build_ui()
    map_demo.run()
