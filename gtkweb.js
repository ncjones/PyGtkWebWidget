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

	/**
	 * Fire an event to the GTK web view widget.
	 * <p>
	 * Messages are transmitted as JSON via the document title.
	 *
	 * @param type {String} the event type
	 * @param data {object} the data attached to the event
	 */
	var fireEvent = function (type, data) {
		document.title = JSON.stringify({
			type: type,
			data: data
		});
	}

	/**
	 * GtkWebWidget JavaScript API.
	 */
	GtkWebWidget = {
		fireEvent: fireEvent
	};

}());

