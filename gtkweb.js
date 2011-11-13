/*
 * Copyright 2011 Nathan Jones
 *
 * This file is part of PyGtkWebWidget.
 *
 * PyGtkWebWidget is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * PyGtkWebWidget is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with PyGtkWebWidget.  If not, see <http://www.gnu.org/licenses/>.
 */

(function () {
	
	var impl = {},
	
	forceTitleChange = false,
	
	registerImplementation = function (obj) {
		impl = obj;
	},

	_sendMessage = function (messageType, messageContent) {
		forceTitleChange = !forceTitleChange;
		document.title = JSON.stringify({
			"message-type": messageType,
			"message-content": messageContent,
			/*
			 * Two consecutive identical messages will not trigger a title change event
			 * so we force the title to change by including the toggled "force change"
			 * flag in the message.
			 */
			"_": forceTitleChange
		});
	},

	fireEvent = function (type, data) {
		_sendMessage("event", {
			"event-type": type,
			"event-data": data || null
		});
	},

	invokeMethod = function (methodName, args) {
		var f = impl[methodName],
			result,
			status;
		try {
			result = f.apply(impl, args);
			status = "success";
		} catch (e) {
			// TODO send entire exception, preserving stack trace
			result = e.message;
			status = "failure";
		}
		_sendMessage("result", {
			"result-status": status,
			"result-value": result || null
		});
	};

	/**
	 * GtkWebWidget JavaScript API.
	 */
	GtkWebWidget = {
			
		/**
		 * Register an object that implements the specific widget. The object
		 * provides the methods that can be invoked on the widget.
		 * <p>
		 * This method should only be called from JavaScript code.
		 *
		 * @param obj {object} the widget implementation.
		 */
		register: registerImplementation,
		
		/**
		 * Notify the GTK web view widget of an event.
		 * <p>
		 * This method should only be called from JavaScript code.
		 *
		 * @param type {String} the event type.
		 * @param data {object} the data attached to the event (optional).
		 */
		fire: fireEvent,
		
		/**
		 * Invoke a method on the JavaScript widget implementation and send the
		 * result to the GTK web view widget.
		 * <p>
		 * If invokation fails, the exception will be sent instead.
		 * <p>
		 * This method should never be called directly from JavaScript code.
		 *
		 * @param methodName {String} the name of the method to invoke.
		 * @param args {array} the arguments to apply to the method.
		 */
		invoke: invokeMethod
		
	};

}());

