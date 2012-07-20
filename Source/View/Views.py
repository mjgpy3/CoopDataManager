#!/usr/bin/env python
import sys
sys.path.append('../Controller')
from ModelAbstraction import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade    
import ViewBrain

class MainWindow:
	""" 
		The main window of the GUI. This is where the user selects the table they want to modify and they determine what they
        	Want to do with said table
	"""
	def __init__(self, tables):
		self.DesiredTable = None

		# Handle the window itself		
		self.GladeFile = 'MainWindow.glade'    
		self.wTree = gtk.glade.XML(self.GladeFile)
		self.Window = self.wTree.get_widget('wdwMain')
		self.Window.set_resizable(False)
		self.Window.connect('destroy', lambda x: gtk.main_quit())
		
		# Handle the combo box
		self.cmbSelectedTable = self.wTree.get_widget('cmbSelectedTable')
		self.cmbSelectedTable.set_active(0)
		for table in tables:
			self.cmbSelectedTable.append_text(table.Name)
		self.cmbSelectedTable.connect('changed', self.UserSelectsDifferentTable)		

		# Handle the quit button
		self.btnQuit = self.wTree.get_widget('btnQuit')
		self.btnQuit.connect('clicked', lambda x: gtk.main_quit())

		self.Window.show_all()    

	def UserSelectsDifferentTable(self, sender):
		self.DesiredTable = self.cmbSelectedTable.get_active_text()	

class NewTableWindow:
	def __init__(self, tableName, attributes):
		self.AttributeRows = []

		# Handle the window itself
		self.GladeFile = 'NewEntry.glade'
		self.wTree = gtk.glade.XML(self.GladeFile)
                self.Window = self.wTree.get_widget('wdwNewEntry')
		self.Window.set_title('Add New ' + tableName)
		self.Window.set_resizable(False)
		self.Window.connect('destroy', lambda x: gtk.main_quit())

		# Create the master Vertical Box
		self.MasterVBox = gtk.VBox()
		for attribute in attributes:
			hbox = gtk.HBox()
			label = gtk.Label()
			label.set_text(ViewBrain.FormatCamelTableName(attribute) + ':')
			entry = gtk.Entry()	
			hbox.add(label)
			hbox.add(entry)
			self.AttributeRows.append(hbox)
			self.MasterVBox.add(hbox)
	
		self.LastHBox = gtk.HBox()
		self.btnSave = gtk.Button('Save')
		self.btnCancel = gtk.Button('Cancel')
		self.btnCancel.connect('clicked', lambda x: gtk.main_quit())

		self.LastHBox.add(self.btnSave)
		self.LastHBox.add(self.btnCancel)
		
		self.MasterVBox.add(self.LastHBox)

		self.Window.add(self.MasterVBox)

		self.Window.show_all()


if __name__ == '__main__':
	# Get an abstraction of the model's structure
	structure = ModelStructure()
	structure.FillTablesFromRawData()

	# Start the main window
	window = MainWindow(structure.Tables)
	gtk.main()

	newEntryWindow = NewTableWindow(window.DesiredTable, structure.GetAttributesListByName(window.DesiredTable))

	gtk.main()
