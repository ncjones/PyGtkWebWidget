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

class SimpleWebWidget(gtkweb.WebWidget):
	  
	__gsignals__ = {
				"click" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
			}
	
	def __init__(self):
		gtkweb.WebWidget.__init__(self, "file://" + os.path.abspath("demo_simple.html"))
	
	def handle_event(self, event_type, event_data):
		if event_type == "click":
			timestamp = float(event_data)/1000
			date_time = datetime.datetime.fromtimestamp(timestamp)
			self.emit("click", date_time)
			
	def get_click_count(self):
		return self.invoke("getClickCount")
			
class SimpleDemo(demo.DemoApp):
	
	def __init__(self):
		self._web_widget = SimpleWebWidget()
		self._web_widget.connect("click", self._on_click)
		
	def get_title(self):
		return "Simple Demo"
    
	def get_description(self):
		return """Demonstrates message passing between Python and JavaScript in an embedded HTML page.

Click events are logged in the console."""
	
	def get_content(self):
		return self._web_widget
		
	def _on_click(self, widget, date_time):
		print "clicked: ", date_time
		print "click count: " , self._web_widget.get_click_count()

if __name__ == '__main__':
	demo = SimpleDemo()
	demo.build_ui()
	demo.run()
