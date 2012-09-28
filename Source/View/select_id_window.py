#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Thu Sep 27 23:22:37 EDT 2012
# 
# 

"""
    In charge of presenting a user with a table's worth of data and allowing them to select only one
row of the data.
"""

import pygtk
pygtk.require('2.0')
import gtk
import sys
sys.path.append('../Controller')

import glade_window
import data_formatters


class SelectIdWindow(glade_window.GladeWindow):
    """
        A window used for selecting a foreign tuple, of which the key (ROWID) is desired.
    """
    def __init__(self, hidden = True):
        # Non-widget data
        self.highlighted = None
        self.text_view = ['None Selected...']

        glade_window.GladeWindow.__init__(self, 'SelectIdWindow.glade')

        # Get the widgets
        self.window = self.connect_widget_by_name('wdwSelectId', 'destroy', lambda x: gtk.main_quit())
        self.connect_widget_by_name('btnOK', 'clicked', self.id_found)
        self.connect_widget_by_name('btnCancel', 'clicked', self.cancel_selection)
        self.header = self.wTree.get_widget('lblTable')
        self.scw_table_case = self.wTree.get_widget('scwTableCase')
        self.selected = self.wTree.get_widget('lblSelected')

        # Run set attributes on the widgets
        self.selected.set_text(self.text_view[0])

    def add_table_data(self, table_data):
        """
            Adds all necessary table data to the window. Ought to be used before displaying.
        """
        # Create a table to later pack with entries
        self.table = gtk.Table()

        # Loop through the headers and add them to the first row of the table
        for index in range(table_data.number_of_attributes):
            button = gtk.Button(str(data_formatters.camel_to_readable(str(table_data.header[index]))))
            button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('yellow'))
            self.table.attach(button, index, index + 1, 0, 1)

        for t in range(table_data.number_of_tuples):
            temp_list = []
            for a in range(table_data.number_of_attributes):
                button = gtk.Button(str(table_data.data[t][a]))
                temp_list.append(str(table_data.data[t][a]))
                self.table.attach(button, a, a + 1, t + 1, t + 2)
                button.connect('clicked', self.change_highlighted, t)
            self.text_view.append(', '.join(temp_list))

        self.scw_table_case.add_with_viewport(self.table)

    def change_highlighted(self, sender, tuple_number):
        """
            Sets the correct ROWID when a user selects a differing one
        """
        self.highlighted = tuple_number + 1
        self.selected.set_text(self.text_view[tuple_number + 1])

    def id_found(self, sender):
        """
            Triggered when a user actually finds the ID they want
        """
        if self.highlighted != None:
            self.window.hide()
            gtk.main_quit()

    def cancel_selection(self, sender):
        """
            Triggered when a user wants to quit browsing for an id
        """
        self.highlighted = None
        self.window.hide()
        gtk.main_quit()

