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

class SimpleDemo(demo.DemoApp):
	
	def __init__(self):
		demo_uri = "file://" + os.path.abspath('demo_simple.html')
		self._web_widget = gtkweb.WebWidget(demo_uri)
		self._web_widget.subscribe("click", self._on_click)
		
	def get_title(self):
		return "Simple Demo"
    
	def get_description(self):
		return """Demonstrates message passing between Python and JavaScript in an embedded HTML page.

Click events are logged in the console."""
	
	def get_content(self):
		return self._web_widget
		
	def _on_click(self, timestamp):
		print "clicked: ", datetime.datetime.fromtimestamp(float(timestamp)/1000)
		print "click count: " , self._web_widget.invoke("getClickCount")

if __name__ == '__main__':
	demo = SimpleDemo()
	demo.build_ui()
	demo.run()
