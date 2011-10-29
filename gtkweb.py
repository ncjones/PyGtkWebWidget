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
import simplejson
import webkit

class WebWidget(webkit.WebView):

	# TODO don't extend WebView
	
	"""A GTK widget that is rendered by a web page.

	The widget provides an interface to a JavaScript object within the page
	to allow JavaScript method invokation and event subscription.

	The widget is not thread safe.
	"""

	def __init__(self, uri):
		webkit.WebView.__init__(self)
		self.connect("title-changed", self._on_title_changed)
		self.load_uri(uri)
		self._events = {}
		self._result_stack = []

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
			self._handle_event(message_content["event-type"], message_content["event-data"])
		elif message_type == "result":
			self._handle_result(message_content["result-status"], message_content["result-value"])

	def _handle_event(self, event_type, event_data):
		self._get_event(event_type).fire(event_data)

	def _handle_result(self, status, value):
		self._result_stack.append(_InvokationResult(status == "success", value))

	def subscribe(self, event_type, callback):
		"""Subscribe to an event published by the widget."""
		# TODO use GTK connect
		self._get_event(event_type).subscribe(callback)

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

class _InvokationResult(object):

	def __init__(self, success, value):
		self.success = success
		self.value = value

class InvokationFailure(Exception):

	def __init__(self, javascriptError):
		Exception.__init__(self, str(javascriptError))

class _Event(object):

    """An event which can be subscribed to for notifications."""

    def __init__(self):
        self.subscribers = []

    def subscribe(self, callback):
        """Subscribe a callback function to the event."""
        self.subscribers.append(callback)

    def unsubscribe(self, callback):
        """Unsubscribe a callback from the event."""
        self.subscribers.remove(callback)

    def fire(self, *args, **kwargs):
        """Notify all subscribers that the event has occurred."""
        return [subscriber(*args, **kwargs) for subscriber in self.subscribers]

