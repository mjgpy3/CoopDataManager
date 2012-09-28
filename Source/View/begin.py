#!/usr/bin/env python

"""
    This module contains the program's main execution loop and that is all. The version you now
see is a vast improvement, and is really only used for testing purposes (usually in an end-to-end
manner or to test a single new feature). It somewhat resembles what the final execution loop will
look like.
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
import reports_window as r
import alert_window as a

if __name__ == '__main__':
    # Get an abstraction of the model's structure
    structure = model_abstraction.ModelStructure()
    structure.build_from_schema()
    config_handler = ConfigHandler('dataMan.conf', {'name':'DataMan'})

    if not config_handler.config_file_exists():
       config_handler.update_config() 

    config_handler.parse_config()
    main_window = m.MainWindow(structure.tables, structure.transaction_tables, config_handler.config['name'])
    alert_window = a.AlertWindow()
    reports_window = r.ReportsWindow(reports.get_current_reports())
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
