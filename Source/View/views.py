#!/usr/bin/env python
import sys
sys.path.append('../Controller')
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade    

import data_formatters
import actions
import queries
from model_abstraction import *
from controller_exceptions import *

class MainWindow:
    """ 
        The main window of the GUI. This is where the user selects the table they want to modify and they determine what they
        Want to do with said table
    """
    def __init__(self, tables):
        # Non-widget data
        self.desired_table = None
        self.current_action = actions.table['None'] 
        self.glade_file = 'MainWindow.glade'

        # Get the widget tree from the glade file
        self.wTree = gtk.glade.XML(self.glade_file)

        # Get the widgets from the wTree
        self.window = self.wTree.get_widget('wdwMain')
        self.cmb_selected_table = self.wTree.get_widget('cmbSelectedTable')
        self.btn_quit = self.wTree.get_widget('btnQuit')
        self.btn_edit = self.wTree.get_widget('btnEdit')
        self.btn_new = self.wTree.get_widget('btnNew')

        # Fill the combobox with the table names
        self.cmb_selected_table.set_active(0)
        for table in tables:
            self.cmb_selected_table.append_text(table.name)

        # Make Connections
        self.window.connect('destroy', self.end_this_window)
        self.cmb_selected_table.connect('changed', self.use_different_table)        
        self.btn_quit.connect('clicked', self.end_this_window)
        self.btn_edit.connect('clicked', self.edit_table)
        self.btn_new.connect('clicked', self.create_new_entry)

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
        if self.cmb_selected_table.get_active() != 0:
            self.current_action = actions.table['New']
        else:
            self.current_action = actions.table['None']
        gtk.main_quit()

class NewTableWindow:
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
        self.glade_file = 'NewEntry.glade'

        # Handle the window itself
        self.wTree = gtk.glade.XML(self.glade_file)
        self.window = self.wTree.get_widget('wdwNewEntry')
        self.window.set_title('Add New ' + table_name)
        self.window.set_resizable(False)
        self.window.connect('destroy', lambda x: gtk.main_quit())
        self.select_id_window = SelectIdWindow()

        # Create the master Vertical Box
        self.master_vbox = gtk.VBox()
        for attribute in attributes:
            hbox, label, entry = gtk.HBox(), gtk.Label(), gtk.Entry()
            label.set_text(data_formatters.camel_to_readable(attribute.name) + ':')
            for widget in [label, entry]:
                hbox.add(widget)
            if attribute.name in self.model_structure.get_table_by_name(self.table_name).references:
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
        self.btn_save = gtk.Button('Save')
        self.btn_save.connect('clicked', self.save_data)
        self.btn_cancel = gtk.Button('Cancel')
        self.btn_cancel.connect('clicked', lambda x: gtk.main_quit())

        self.last_hbox.add(self.btn_save)
        self.last_hbox.add(self.btn_cancel)
            
        self.master_vbox.add(self.last_hbox)

        self.window.add(self.master_vbox)

        self.window.show_all()

    def save_data(self, sender):
        self.current_action = actions.table['New']
        gtk.main_quit()
        
    def attribute_changed(self, sender, attribute):
        self.set_attributes[attribute] = sender.get_text()

    def browse_for_id(self, sender, attr_name, entry):
        table_data = queries.SelectQuery().get_all_data_from_table(self.model_structure.get_table_by_name(self.table_name).references[str(attr_name)]) 
        self.select_id_window.add_table_data(table_data)
        self.select_id_window.window.show_all()
        gtk.main()
        if self.select_id_window.highlighted != None:
            self.set_attributes[self.model_structure.get_attribute_from_table(attr_name, self.table_name)] = self.select_id_window.highlighted
            entry.set_text(str(self.select_id_window.highlighted))

    def clear_id(self, sender, attr_name, entry):
        self.set_attributes[self.model_structure.get_attribute_from_table(attr_name, self.table_name)] = ''
        entry.set_text('')
        self.select_id_window.highlighted = None

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

class SelectIdWindow:
    """
        A window used for selecting a foreign tuple, of which the key (ROWID) is desired.
    """
    def __init__(self, hidden = True):
        # Non-widget data
        self.highlighted = None
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
        self.highlighted = tuple_number + 1
        self.selected.set_text(self.text_view[tuple_number + 1])

    def id_found(self, sender):
        if self.highlighted != None:
            self.window.hide()
            gtk.main_quit()

    def cancel_selection(self, sender):
        self.highlighted = None
        self.window.hide()
        gtk.main_quit()

if __name__ == '__main__':
    # Get an abstraction of the model's structure
    structure = ModelStructure()

    main_window = MainWindow(structure.tables)
    alert_window = AlertWindow()
    insert = queries.InsertQuery()
    for wh in [main_window, alert_window]:
        wh.window.hide()


    while True:
        main_window.window.show()
        gtk.main()
        main_window.window.hide()
        if main_window.current_action == actions.table['New']:
            new_table_window = NewTableWindow(main_window.desired_table, structure.get_attributes_list_by_name(main_window.desired_table), structure)
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

            elif new_table_window.current_action == actions.table['New']:
                alert_window.label.set_text('No data entered, nothing was saved.')
                alert_window.window.show_all()
                gtk.main()
        elif main_window.current_action == actions.table['Edit']:
            print "Clicked Edit"
        elif main_window.current_action == actions.table['Quit']:
            break
