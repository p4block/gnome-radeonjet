#!/usr/bin/env python3
# __main__.py
#
# Copyright (C) 2016 pablo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.	If not, see <http://www.gnu.org/licenses/>.

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import subprocess
from subprocess import check_output

class Application(Gtk.Application):
	def __init__(self, **kwargs):
		super().__init__(application_id='com.siliconframe.Radeonjet',
		**kwargs)

	def do_activate(self):
		window = LandingWindow(self)
		window.show_all()

class LandingWindow(Gtk.Window):

	def __init__(self, app):
		Gtk.Window.__init__(self, title="RadeonJet", application=app)
		self.set_default_size(500, 800)
		self.set_border_width(20)

		self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		self.add(self.box)

		self.box_columns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.box.add(self.box_columns)

		self.box_column1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		self.box_columns.pack_start(self.box_column1, True, True, 0)

		self.box_column2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		self.box_columns.pack_start(self.box_column2, True, True, 0)



		core_clock = subprocess.check_output(["radeonjet", "get", "core"])
		self.core_label = Gtk.Label(core_clock, halign=Gtk.Align.START)
		self.box_column1.pack_start(self.core_label, True, True, 0)

		memory_clock = subprocess.check_output(["radeonjet", "get", "memory"])
		self.memory_label = Gtk.Label(memory_clock, halign=Gtk.Align.START)
		self.box_column2.pack_start(self.memory_label, True, True, 0)

		core_braveness_range = Gtk.Adjustment(0, 0, 20, 1, 10, 0) ##GET BRAVENESS VALUE
		memory_braveness_range = Gtk.Adjustment(0, 0, 20, 1, 10, 0) ##GET BRAVENESS VALUE

		self.core_oc_selector = Gtk.SpinButton()
		self.core_oc_selector.set_adjustment(core_braveness_range)
		self.box_column1.pack_start(self.core_oc_selector, True, True, 0)

		self.memory_oc_selector = Gtk.SpinButton()
		self.memory_oc_selector.set_adjustment(memory_braveness_range)
		self.box_column2.pack_start(self.memory_oc_selector, True, True, 0)

		self.core_table = Gtk.ListBox()
		self.box_column1.add(self.core_table)

		self.memory_table = Gtk.ListBox()
		self.box_column2.add(self.memory_table)

		core_table = subprocess.check_output(["radeonjet", "get", "core", "table"])
		row = Gtk.ListBoxRow()






		self.ResetButton = Gtk.Button(label="RESET")
		self.ResetButton.connect("clicked", self.on_ResetButton_clicked)
		self.box.pack_start(self.ResetButton, True, True, 0)

	def on_ResetButton_clicked(self, widget):
		subprocess.check_output(["radeonjet", "reset"])

def main():
	application = Application()

	try:
		ret = application.run(sys.argv)
	except SystemExit as e:
		ret = e.code

	sys.exit(ret)

if __name__ == '__main__':
	main()
