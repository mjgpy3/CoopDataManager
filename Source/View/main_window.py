#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Thu Sep 27 22:47:41 EDT 2012
# 
# 

"""
    What the user sees first. It's in charge of allowing the user the ability to switch through
different features offered in this data manager.
"""

import pygtk
pygtk.require('2.0')
import gtk

import glade_window
import actions


class MainWindow(glade_window.GladeWindow):
    """ 
        The main window of the GUI. This is where the user selects the table they want to modify and they determine what they
        Want to do with said table
    """
    def __init__(self, tables, t_tables, window_name = ''):
        # Non-widget data
        self.desired_table = None
        self.current_action = actions.table['None'] 
        glade_window.GladeWindow.__init__(self, 'MainWindow.glade')

        # Get the widgets from the wTree
        self.window = self.connect_widget_by_name('wdwMain', 'destroy', self.end_this_window)
        self.cmb_selected_table = self.connect_widget_by_name('cmbSelectedTable', \
                                                              'changed', self.use_different_table)
        # Get the buttons and connect 'em thanks to inheritance!
        self.btn_quit = self.connect_widget_by_name('btnQuit', 'clicked', self.end_this_window)
        self.btn_edit = self.connect_widget_by_name('btnEdit', 'clicked', self.edit_table)
        self.btn_new = self.connect_widget_by_name('btnNew', 'clicked', self.create_new_entry)
        self.btn_reports = self.connect_widget_by_name('btnReports', 'clicked', self.generate_reports)
        self.btn_defaults = self.connect_widget_by_name('btnDefaults', 'clicked', self.edit_defaults)

        # Fill the combobox with the table names
        self.cmb_selected_table.set_active(0)
        for table in tables + t_tables:
            self.cmb_selected_table.append_text(table.name)

	self.window.set_title(window_name)

    def end_this_window(self, sender):
        """
            Simply ends this window.
        """
        self.current_action = actions.table['Quit']
        gtk.main_quit()

    def use_different_table(self, sender):
        """
            Switches the DesiredTable data member whenever the user selects a different one in the
            selection box.
        """
        self.desired_table = self.cmb_selected_table.get_active_text()
        if self.cmb_selected_table.get_active() != 0:
            self.btn_edit.set_label('Edit ' + self.desired_table + ' Table')
            self.btn_new.set_label('New ' + self.desired_table)
        else:
            self.btn_edit.set_label('Edit...')
            self.btn_new.set_label('New...')

    def edit_table(self, sender):
        """
            Handles the "Edit" button when it is clicked.
        """
        self.current_action = actions.table['Edit']
        gtk.main_quit()

    def create_new_entry(self, sender):
        """
            Handles the "New" button when it is clicked.
        """
        self.set_action_if_real_table_selected(actions.table['New'])
        gtk.main_quit()

    def edit_defaults(self, sender):
        """
            Handles the "Defaults" button when it is clicked
        """
        self.set_action_if_real_table_selected(actions.table['Defaults'])
        gtk.main_quit()

    def generate_reports(self, sender):
        """
            Handles the "Reports" button when it is clicked
        """
        self.current_action = actions.table['Reports']
        gtk.main_quit()

    def set_action_if_real_table_selected(self, action):
        """
            Sets the current action to the passed iff a valid
            table is selected.
        """
        if self.cmb_selected_table.get_active() != 0:
            self.current_action = action
        else:
            self.current_action = actions.table['None']
