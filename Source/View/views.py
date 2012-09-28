#!/usr/bin/env python

"""
    This module contains all view classes and the program's main execution loop. It needs to be separated and is not complete.
    Each *Window class will have its own module (.py file) and the main program will no longer be stored here
"""

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

import glade_window
import main_window as m
import new_table_window as n

class AlertWindow:
    """
        The window used for displaying errors and other warnings.
    """
    def __init__(self, alert_string = 'Sorry!\nAn Unknown Error Has Occured.'):
        # Non-widget data
        self.glade_file = 'AlertWindow.glade'

        # Get the widget tree
        self.wTree = gtk.glade.XML(self.glade_file)

        # Get the widgets
        self.window = self.wTree.get_widget('wdwAlert')
        self.label = self.wTree.get_widget('lblAlertText')
        self.btn_quit = self.wTree.get_widget('btnOkay')

        # Set attributes of the widgets
        self.window.set_resizable(False)
        self.window.set_title('Error...')    
        self.label.set_text(alert_string)

        # Make connections
        self.window.connect('destroy', lambda x: gtk.main_quit())
        self.btn_quit.connect('clicked', self.quit_this_window)

    def quit_this_window(self, sender):
        """
            Handles exiting the window
        """
        self.window.hide()
        gtk.main_quit()

class ReportsWindow(glade_window.GladeWindow):
    """
        A window which allows the user to select known reports and generate them.
    """
    def __init__(self, reports):
        # Non-widget data
        self.highlighted = None
        self.reports = reports
        self.current_action = actions.table['None']

        glade_window.GladeWindow.__init__(self, 'ReportsWindow.glade')

        # Get the widgets
        self.window = self.connect_widget_by_name('wdwReports', 'destroy', lambda x: gtk.main_quit())
        self.btn_generate = self.connect_widget_by_name('btnGenerate', 'clicked', lambda x: gtk.main_quit())
        self.btn_cancel = self.connect_widget_by_name('btnCancel', 'clicked', self.quit_this_window)
        self.cmb_select_reports = self.connect_widget_by_name('cmbSelectReports', \
                                                              'changed', self.set_different_report)

        # Set the combobox's entires
        for report in reports:
            self.cmb_select_reports.append_text(report.name + ' - ' + report.output_format)
        self.window.set_title('Reports')
        self.cmb_select_reports.set_active(0)
        self.cmb_select_reports.set_visible(True)

    def set_different_report(self, sender):
        """
            Sets the current report if the user changed it to a valid option
        """
        if self.cmb_select_reports.get_active() != 0:
            self.highlighted = self.reports[self.cmb_select_reports.get_active() - 1]
            self.current_action = actions.table['Reports']
        else:
            self.current_action = actions.table['Quit']

    def quit_this_window(self, sender):
        """
            Handles quitting the window
        """
        self.current_action = actions.table['Quit']
        gtk.main_quit()

if __name__ == '__main__':
    # Get an abstraction of the model's structure
    structure = model_abstraction.ModelStructure()
    structure.build_from_schema()
    config_handler = ConfigHandler('dataMan.conf', {'name':'DataMan'})

    if not config_handler.config_file_exists():
       config_handler.update_config() 

    config_handler.parse_config()
    main_window = m.MainWindow(structure.tables, structure.transaction_tables, config_handler.config['name'])
    alert_window = AlertWindow()
    reports_window = ReportsWindow(reports.get_current_reports())
    insert = queries.InsertQuery(structure)
    for wh in [main_window, alert_window, reports_window]:
        wh.window.hide()

    while True:
        main_window.window.show()
        gtk.main()
        main_window.window.hide()
        if main_window.current_action == actions.table['New']:
            new_table_window = n.NewTableWindow(main_window.desired_table, structure.get_attributes_list_by_name(main_window.desired_table), structure)
            gtk.main()
            new_table_window.window.hide()
            print new_table_window.set_attributes
            if ((new_table_window.current_action == actions.table['New']) and
               len([i for i in new_table_window.set_attributes if new_table_window.set_attributes[i] not in [None, '']]) != 0):
                try:
                    insert.insert_from_dictionary(main_window.desired_table, new_table_window.set_attributes)
                except ImproperDataError as e:
                    alert_window.label.set_text(str(e))
                    alert_window.window.show_all()
                    gtk.main()
                except sqlite3.IntegrityError as e:
                    alert_window.label.set_text(str(e))
                    alert_window.window.show_all()
                    gtk.main()

            elif new_table_window.current_action == actions.table['New']:
                alert_window.label.set_text('No data entered, nothing was saved.')
                alert_window.window.show_all()
                gtk.main()
        elif main_window.current_action == actions.table['Edit']:
            print "Clicked Edit"
        elif main_window.current_action == actions.table['Reports']:
            reports_window.window.show_all()
            gtk.main()
            reports_window.window.hide()
            if reports_window.current_action not in [actions.table['Quit'], actions.table['None']]:
                reports_window.highlighted.generator()
        elif main_window.current_action == actions.table['Defaults']:
            print "Valid Defaults Clicked"
        elif main_window.current_action == actions.table['Quit']:
            break
