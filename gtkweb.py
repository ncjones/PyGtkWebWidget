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

import gobject
import gtk
import simplejson
import webkit

class WebWidget(webkit.WebView):

	# TODO don't extend WebView
	
	"""A GTK widget that is rendered by a web page.

	The widget provides an interface to a JavaScript object within the page
	to allow JavaScript method invokation and event subscription.

	The widget is not thread safe.
	"""
	
	__gproperties__ = {
				"uri" : (gobject.TYPE_STRING,
						"Document URI",
						"The URI for the widget's HTML document.",
						None,
						gobject.PARAM_READWRITE)
			}

	def __gobject_init__(self, **kwargs):
		webkit.WebView.__gobject_init__(self, **kwargs)
		self.connect("title-changed", self._on_title_changed)
		self._result_stack = []
		
	def render(self):
		self.load_uri(self.get_property("uri"))
		
	def do_get_property(self, property):
		if property.name == "uri":
			return self.uri
		else:
			raise AttributeError, "Unknown property: %s" % property.name
		
	def do_set_property(self, property, value):
		if property.name == "uri":
			self.uri = value
		else:
			raise AttributeError, "Unknown property: %s" % property.name

	def _get_event(self, event_type):
		if not event_type in self._events:
			self._events[event_type] = _Event()
		return self._events[event_type]

	def _on_title_changed(self, view, frame, title):
		message = simplejson.loads(title)
		message_type = message["message-type"]
		message_content = message["message-content"]
		if message_type == "event":
			# TODO check if event data is present
			self.handle_event(message_content["event-type"], message_content["event-data"])
		elif message_type == "result":
			self._handle_result(message_content["result-status"], message_content["result-value"])
			
	def handle_event(self, event_type, event_data):
		pass

	def _handle_result(self, status, value):
		self._result_stack.append(_InvokationResult(status == "success", value))

	def invoke(self, function_name, *args):
		"""Invoke a JavaScript method on the widget."""
		# TODO use namespace for function
		script = "GtkWebWidget.invoke(" + simplejson.dumps(function_name) + ", " + simplejson.dumps(args) + ")"
		self.execute_script(script)
		result = self._result_stack.pop()
		if result.success:
			return result.value
		else:
			raise InvokationFailure(result.value)
		
gobject.type_register(WebWidget)

class _InvokationResult(object):

	def __init__(self, success, value):
		self.success = success
		self.value = value

class InvokationFailure(Exception):

	def __init__(self, javascriptError):
		Exception.__init__(self, str(javascriptError))
