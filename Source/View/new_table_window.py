#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Thu Sep 27 23:14:58 EDT 2012
# 
# 

"""
    In charge of creating a form for the user to enter data into to be saved in the model (through
the controller of course). The form also allows foreign references to be browsed for and entered
easily.
"""

import pygtk
pygtk.require('2.0')
import gtk
import sys
sys.path.append('../Controller')

import data_formatters
import glade_window
import actions
import queries
import select_id_window as sid

class NewTableWindow(glade_window.GladeWindow):
    """
        This window allows users to create new table entries. It automatially generates a form for some passed table name
        and list of attributes.
    """
    def __init__(self, table_name, attributes, model_structure):
        # Non-widget data
        self.set_attributes = {}
        self.model_structure = model_structure
        self.current_action = actions.table['None']
        self.table_name = table_name

        glade_window.GladeWindow.__init__(self, 'NewEntryWindow.glade')

        # Handle the window itself
        self.window = self.connect_widget_by_name('wdwNewEntry', 'destroy', lambda x: gtk.main_quit())
        self.window.set_title('Add New ' + table_name)
        self.window.set_resizable(False)

        # Create the master Vertical Box
        self.master_vbox = gtk.VBox()
        references = self.model_structure.get_table_by_name(self.table_name).references
        for attribute in attributes:
            hbox, label, entry = gtk.HBox(), gtk.Label(), gtk.Entry()
            label.set_text(data_formatters.camel_to_readable(attribute.name) + ':')
            for widget in [label, entry]:
                hbox.add(widget)
            if attribute.acceptable_values != None:
                cmb = gtk.combo_box_new_text()
                for value in attribute.acceptable_values:
                    cmb.append_text(str(value))
                self.set_attributes[attribute] = attribute.acceptable_values[0]
                cmb.set_active(0)
                cmb.set_visible(True)
                hbox.add(cmb)
                cmb.connect('changed', self.selects_different_value, attribute)
                hbox.remove(entry)
            elif attribute.name in references:
                btn_browse = gtk.Button('Browse')
                btn_clear = gtk.Button('Clear')
                btn_browse.connect('clicked', self.browse_for_id, attribute.name, entry)
                btn_clear.connect('clicked', self.clear_id, attribute.name, entry)
                entry.set_editable(False)
                hbox.add(btn_browse)
                hbox.add(btn_clear)
            else:
                hbox.add(label)
                hbox.add(entry)
                self.set_attributes[attribute] = ''
                entry.connect('changed', self.attribute_changed, attribute)
            self.master_vbox.add(hbox)
    
        self.last_hbox = gtk.HBox()
        self.btn_save = self.connect_new_button('Save', self.save_data)
        self.btn_cancel = self.connect_new_button('Cancel', lambda x: gtk.main_quit())
        self.last_hbox.add(self.btn_save)
        self.last_hbox.add(self.btn_cancel)
            
        self.master_vbox.add(self.last_hbox)

        self.window.add(self.master_vbox)

        self.window.show_all()

    def save_data(self, sender):
        """
            Handles ending the window when the user would like to save data
        """
        self.current_action = actions.table['New']
        gtk.main_quit()
        
    def attribute_changed(self, sender, attribute):
        """
            Changes the dictionary that will be written whenever a user changes a connected entry field
        """
        self.set_attributes[attribute] = sender.get_text()

    def selects_different_value(self, sender, attribute):
        self.set_attributes[attribute] = sender.get_active_text()

    def browse_for_id(self, sender, attr_name, entry):
        """
            Starts the necessary actions when the user wants to browse for an id
        """
        table_data = queries.SelectQuery(self.model_structure).get_all_data_from_table(self.model_structure.get_table_by_name(self.table_name).references[str(attr_name)]) 
        select_id_window = sid.SelectIdWindow()
        select_id_window.add_table_data(table_data)
        select_id_window.window.show_all()
        gtk.main()
        if select_id_window.highlighted != None:
            self.set_attributes[self.model_structure.get_attribute_from_table(attr_name, self.table_name)] = select_id_window.highlighted
            entry.set_text(str(select_id_window.highlighted))

    def clear_id(self, sender, attr_name, entry):
        """
            Clears out the entry when the user decides they don't want a previously selected ID
        """
        self.set_attributes[self.model_structure.get_attribute_from_table(attr_name, self.table_name)] = ''
        entry.set_text('')

