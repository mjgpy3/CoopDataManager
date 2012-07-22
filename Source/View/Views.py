#!/usr/bin/env python
import sys
sys.path.append('../Controller')
from ModelAbstraction import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade    
import ViewBrain, Actions

class MainWindow:
	""" 
		The main window of the GUI. This is where the user selects the table they want to modify and they determine what they
        	Want to do with said table
	"""
	def __init__(self, tables):
		self.DesiredTable = None
		self.CurrentAction = Actions.Table['None'] 

		# Handle the window itself		
		self.GladeFile = 'MainWindow.glade'    
		self.wTree = gtk.glade.XML(self.GladeFile)
		self.Window = self.wTree.get_widget('wdwMain')
		self.Window.set_resizable(False)
		self.Window.connect('destroy', self.EndThisWindow)
		
		# Handle the combo box
		self.cmbSelectedTable = self.wTree.get_widget('cmbSelectedTable')
		self.cmbSelectedTable.set_active(0)
		for table in tables:
			self.cmbSelectedTable.append_text(table.Name)
		self.cmbSelectedTable.connect('changed', self.UserSelectsDifferentTable)		

		# Handle the quit button
		self.btnQuit = self.wTree.get_widget('btnQuit')
		self.btnQuit.connect('clicked', self.EndThisWindow)
		self.btnEdit = self.wTree.get_widget('btnEdit')		
		self.btnEdit.connect('clicked', self.UserSelectsEdit)
		self.btnNew = self.wTree.get_widget('btnNew')
                self.btnNew.connect('clicked', self.UserSelectsNew)

		self.Window.show_all()    

	def EndThisWindow(self, sender):
		self.CurrentAction = Actions.Table['Quit']
		gtk.main_quit()

	def UserSelectsDifferentTable(self, sender):
		self.DesiredTable = self.cmbSelectedTable.get_active_text()	

	def UserSelectsEdit(self, sender):
		self.CurrentAction = Actions.Table['Edit']
		gtk.main_quit()

	def UserSelectsNew(self, sender):
		self.CurrentAction = Actions.Table['New']
		gtk.main_quit()

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

class AlertWindow:
	def __init__(self, alertString = 'Sorry!\nAn Unknown Error Has Occured.'):
		self.GladeFile = 'AlertWindow.glade'
                self.wTree = gtk.glade.XML(self.GladeFile)
                self.Window = self.wTree.get_widget('wdwAlert')
                self.Window.set_resizable(False)
                self.Window.connect('destroy', lambda x: gtk.main_quit())	
		self.Window.set_title('Error...')	
		self.label = self.wTree.get_widget('lblAlertText')
		self.btnQuit = self.wTree.get_widget('btnOkay')
		self.btnQuit.connect('clicked', lambda x: gtk.main_quit())
		self.label.set_text(alertString)

		self.Window.show_all()

if __name__ == '__main__':
	# Get an abstraction of the model's structure
	structure = ModelStructure()

	mainWindow = MainWindow(structure.Tables)
	alertWindow = AlertWindow()
	for wh in [mainWindow, alertWindow]:
		wh.Window.hide()


	while True:
		mainWindow.Window.show()
		gtk.main()
		mainWindow.Window.hide()
		if mainWindow.CurrentAction == Actions.Table['New']:
			newTableWindow = NewTableWindow(mainWindow.DesiredTable, structure.GetAttributesListByName(mainWindow.DesiredTable))
			gtk.main()
			newTableWindow.Window.hide()
		if mainWindow.CurrentAction == Actions.Table['Quit']:
			break
