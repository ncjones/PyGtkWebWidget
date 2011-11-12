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

import datetime
import demo
import gobject
import gtk
import gtkweb
import os

class MapWebWidget(gtkweb.WebWidget):
      
    __gsignals__ = {
                "marker-added" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)),
                "marker-selection-changed" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_INT64,))
            }
    
    def __init__(self):
        gtkweb.WebWidget.__gobject_init__(self, uri="file://" + os.path.abspath("demo_maps.html"))
    
    def handle_event(self, event_type, event_data):
        if event_type == "marker-added":
            self.emit("marker-added", MapMarker(**event_data))
        if event_type == "marker-selection-changed":
            self.emit("marker-selection-changed", int(event_data))
            
    def select_marker(self, index):
        self.invoke("selectMarker", index);
            
class MapMarker(object):
    
    def __init__(self, **kwargs):
        self.index = int(kwargs["index"])
        self.latitude = float(kwargs["lat"])
        self.longitude = float(kwargs["lng"])

class MapDemo(demo.DemoApp):
    
    def __init__(self):
        self._web_widget = MapWebWidget()
        self._web_widget.connect("marker-added", self.on_marker_added)
        self._web_widget.connect("marker-selection-changed", self.on_marker_selection_changed)
        self._web_widget.render()
        self._marker_list_store = gtk.ListStore(float, float)
        self._marker_tree_view = self._create_tree_view()
        self._marker_tree_view.get_selection().connect("changed", self.on_marker_tree_selection_changed)
        
    def get_title(self):
        return "Maps Demo"
    
    def get_description(self):
        return """Demonstrates message passing between Python and JavaScript in an embedded HTML page.

On the left is a WebWidget that allows points to be marked on a map. On the right is a GTK TreeView.

Click the map to add a marker. Click a marker to select it. The map and TreeView state will be kept in sync."""
        
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

    def on_marker_added(self, widget, marker):
        self._marker_list_store.insert(marker.index, [marker.latitude, marker.longitude])
        
    def on_marker_selection_changed(self, widget, index):
        iter = self._marker_list_store.get_iter(index)
        self._marker_tree_view.get_selection().select_iter(iter)
    
    def on_marker_tree_selection_changed(self, selection):
        iter = selection.get_selected()[1]
        path = self._marker_list_store.get_path(iter)
        index = path[0]
        self._web_widget.select_marker(index)

if __name__ == '__main__':
    map_demo = MapDemo()
    map_demo.build_ui()
    map_demo.run()
