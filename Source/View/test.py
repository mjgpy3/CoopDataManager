#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Sun Aug 26 20:24:19 EDT 2012
# 
# 

import sys
sys.path.append('../Controller')
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import sqlite3

import data_formatters
import actions
import queries
import model_abstraction
import reports
from controller_exceptions import *
from config_handler import *


class SelectIdWindow:
    """
        A window used for selecting a foreign tuple, of which the key (ROWID) is desired.
    """
    def __init__(self, hidden = True):
        # Non-widget data
        self.id_to_attr_value = {}
        self.text_view = ['None Selected...']
        self.glade_file = 'SelectIdWindow.glade'

        # Get the wtree
        self.wTree = gtk.glade.XML(self.glade_file)

        # Get the widgets
        self.window = self.wTree.get_widget('wdwSelectId')
        self.header = self.wTree.get_widget('lblTable')
        self.scw_table_case = self.wTree.get_widget('scwTableCase')
        self.selected = self.wTree.get_widget('lblSelected')

        # Make connections
        self.wTree.get_widget('btnOK').connect('clicked', self.id_found)
        self.wTree.get_widget('btnCancel').connect('clicked', self.cancel_selection)
        self.window.connect('destroy', lambda x: gtk.main_quit())

        # Run set attributes on the widgets
        self.selected.set_text(self.text_view[0])

    def add_table_data(self, table_data):
        """
            Adds all necessary table data to the window. Ought to be used before displaying.
        """
        # Create a table to later pack with entries
        self.table = gtk.Table()

        # Loop through the headers and add them to the first row of the table
        for index in range(1, table_data.number_of_attributes):
            button = gtk.Button(str(data_formatters.camel_to_readable(str(table_data.header[index]))))
            button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('yellow'))
            self.table.attach(button, index, index + 1, 0, 1)

        for t in range(table_data.number_of_tuples):
            temp_list = []
            for a in range(1, table_data.number_of_attributes):
                entry = gtk.Entry()
                entry.set_text(str(table_data.data[t][a]))
                temp_list.append(str(table_data.data[t][a]))
                self.table.attach(entry, a, a + 1, t + 1, t + 2)
                entry.connect('changed', self.change_made, t)
            self.text_view.append(', '.join(temp_list))

        self.scw_table_case.add_with_viewport(self.table)

    def change_made(self, sender, tuple_number):
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


if __name__ == '__main__':
    test_class = SelectIdWindow()
    model_structure = model_abstraction.ModelStructure()
    model_structure.build_from_schema()
    query = queries.SelectQuery(model_structure)
    test_class.add_table_data(query.get_all_data_from_table("Parent"))
    test_class.window.show_all()
    gtk.main()
