#!/usr/bin/env python
import sys
sys.path.append('../Controller')
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade    

import ViewBrain
import Actions
import Queries
from ModelAbstraction import *
from ControllerExceptions import *

class MainWindow:
	""" 
		The main window of the GUI. This is where the user selects the table they want to modify and they determine what they
        	Want to do with said table
	"""
	def __init__(self, tables):
		# Non-widget data
		self.DesiredTable = None
		self.CurrentAction = Actions.Table['None'] 
		self.GladeFile = 'MainWindow.glade'

		# Get the widget tree from the glade file
		self.wTree = gtk.glade.XML(self.GladeFile)

		# Get the widgets from the wTree
		self.Window = self.wTree.get_widget('wdwMain')
		self.cmbSelectedTable = self.wTree.get_widget('cmbSelectedTable')
		self.btnQuit = self.wTree.get_widget('btnQuit')
		self.btnEdit = self.wTree.get_widget('btnEdit')
		self.btnNew = self.wTree.get_widget('btnNew')
		
		# Fill the combobox with the table names
		self.cmbSelectedTable.set_active(0)
		for table in tables:
			self.cmbSelectedTable.append_text(table.Name)

		# Make Connections
		self.Window.connect('destroy', self.EndThisWindow)
		self.cmbSelectedTable.connect('changed', self.UserSelectsDifferentTable)		
		self.btnQuit.connect('clicked', self.EndThisWindow)
		self.btnEdit.connect('clicked', self.UserSelectsEdit)
                self.btnNew.connect('clicked', self.UserSelectsNew)

	def EndThisWindow(self, sender):
		"""
			Simply ends this window.
		"""
		self.CurrentAction = Actions.Table['Quit']
		gtk.main_quit()

	def UserSelectsDifferentTable(self, sender):
		"""
			Switches the DesiredTable data member whenever the user selects a different one in the
			selection box.
		"""
		self.DesiredTable = self.cmbSelectedTable.get_active_text()	

	def UserSelectsEdit(self, sender):
		"""
			Handles the "Edit" button when it is clicked.
		"""
		self.CurrentAction = Actions.Table['Edit']
		gtk.main_quit()

	def UserSelectsNew(self, sender):
		"""
			Handles the "New" button when it is clicked.
		"""
		if self.cmbSelectedTable.get_active() != 0:
			self.CurrentAction = Actions.Table['New']
		else:
			self.CurrentAction = Actions.Table['None']
		gtk.main_quit()

class NewTableWindow:
	"""
		This window allows users to create new table entries. It automatially generates a form for some passed tableName
		and list of attributes.
	"""
	def __init__(self, tableName, attributes, model_structure):
		# Non-widget data
		self.SetAttributes = {}
		self.ModelStructure = model_structure
		self.CurrentAction = Actions.Table['None']
		self.TableName = tableName
		self.GladeFile = 'NewEntry.glade'

		# Handle the window itself
		self.wTree = gtk.glade.XML(self.GladeFile)
                self.Window = self.wTree.get_widget('wdwNewEntry')
		self.Window.set_title('Add New ' + tableName)
		self.Window.set_resizable(False)
		self.Window.connect('destroy', lambda x: gtk.main_quit())
		self.SelectIdWindow = SelectIdWindow()

		# Create the master Vertical Box
		self.MasterVBox = gtk.VBox()
		for attribute in attributes:
			hbox, label, entry = gtk.HBox(), gtk.Label(), gtk.Entry()
			label.set_text(ViewBrain.FormatCamelTableName(attribute.Name) + ':')
			for widget in [label, entry]:
				hbox.add(widget)
			if 'Id' in attribute.Name:
				button = gtk.Button('Browse')
				buttonClear = gtk.Button('Clear')
				button.connect('clicked', self.UserSelectsBrowse, attribute.Name, entry)
				buttonClear.connect('clicked', self.UserSelectsClear, attribute.Name, entry)
				entry.set_editable(False)
				hbox.add(button)
				hbox.add(buttonClear)
			else:
				hbox.add(label)
				hbox.add(entry)
				self.SetAttributes[attribute] = ''
				entry.connect('changed', self.UserChangesAttribute, attribute)
			self.MasterVBox.add(hbox)
	
		self.LastHBox = gtk.HBox()
		self.btnSave = gtk.Button('Save')
		self.btnSave.connect('clicked', self.UserWantsToCreate)
		self.btnCancel = gtk.Button('Cancel')
		self.btnCancel.connect('clicked', lambda x: gtk.main_quit())

		self.LastHBox.add(self.btnSave)
		self.LastHBox.add(self.btnCancel)
			
		self.MasterVBox.add(self.LastHBox)

		self.Window.add(self.MasterVBox)

		self.Window.show_all()

	def UserWantsToCreate(self, sender):
		self.CurrentAction = Actions.Table['New']
		gtk.main_quit()
		
	def UserChangesAttribute(self, sender, attribute):
		self.SetAttributes[attribute] = sender.get_text()

	def UserSelectsBrowse(self, sender, attrName, entry):
		table_data = None
		table_data = Queries.SelectQuery().GetAllDataFromTable(self.ModelStructure.GetTableByName(self.TableName).References[str(attrName)]) 
		self.SelectIdWindow.AddTableData(table_data)
		self.SelectIdWindow.Window.show_all()
		gtk.main()
		if self.SelectIdWindow.Highlighted != None:
			self.SetAttributes[self.ModelStructure.GetAttributeFromTable(attrName, self.TableName)] = self.SelectIdWindow.Highlighted
			entry.set_text(str(self.SelectIdWindow.Highlighted))

	def UserSelectsClear(self, sender, attrName, entry):
		self.SetAttributes[self.ModelStructure.GetAttributeFromTable(attrName, self.TableName)] = ''
		entry.set_text('')
		self.SelectIdWindow.Highlighted = None

class AlertWindow:
	"""
		The window used for displaying errors and other warnings.
	"""
	def __init__(self, alertString = 'Sorry!\nAn Unknown Error Has Occured.'):
		self.GladeFile = 'AlertWindow.glade'

                self.wTree = gtk.glade.XML(self.GladeFile)
                self.Window = self.wTree.get_widget('wdwAlert')
                self.Window.set_resizable(False)
                self.Window.connect('destroy', lambda x: gtk.main_quit())	
		self.Window.set_title('Error...')	
		self.label = self.wTree.get_widget('lblAlertText')
		self.btnQuit = self.wTree.get_widget('btnOkay')
		self.btnQuit.connect('clicked', self.QuitClicked)
		self.label.set_text(alertString)

	def QuitClicked(self, sender):
		"""
			Handles exiting the window
		"""
		self.Window.hide()
		gtk.main_quit()

class SelectIdWindow:
	"""
		A window used for selecting a foreign tuple, of which the key (ROWID) is desired.
	"""
	def __init__(self, hidden = True):
		self.Highlighted = None
		self.TextView = ['None Selected...']
		self.GladeFile = 'SelectIdWindow.glade'

		self.wTree = gtk.glade.XML(self.GladeFile)
                self.Window = self.wTree.get_widget('wdwSelectId')
		self.Header = self.wTree.get_widget('lblTable')
		self.scwTableCase = self.wTree.get_widget('scwTableCase')
		self.Selected = self.wTree.get_widget('lblSelected')
		self.Selected.set_text(self.TextView[0])
		self.wTree.get_widget('btnOK').connect('clicked', self.OKClicked)
		self.wTree.get_widget('btnCancel').connect('clicked', self.CancelClicked)
		self.Window.connect('destroy', lambda x: gtk.main_quit())

	def AddTableData(self, tableData):
		"""
			Adds all necessary table data to the window. Ought to be used before displaying.
		"""
		# Create a table to later pack with entries
		self.Table = gtk.Table()#0, 0, False)

		# Loop through the headers and add them to the first row of the table
		for index in range(tableData.NumberOfAttributes):
			button = gtk.Button(str(ViewBrain.FormatCamelTableName(str(tableData.Header[index]))))
			button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('yellow'))
			self.Table.attach(button, index, index + 1, 0, 1)

		for tupleIndex in range(tableData.NumberOfTuples):
			tempList = []
			for attrIndex in range(tableData.NumberOfAttributes):
				button = gtk.Button(str(tableData.Data[tupleIndex][attrIndex]))
				tempList.append(str(tableData.Data[tupleIndex][attrIndex]))
				self.Table.attach(button, attrIndex, attrIndex + 1, tupleIndex + 1, tupleIndex + 2)
				button.connect('clicked', self.UserSelectsNew, tupleIndex)
			self.TextView.append(', '.join(tempList))

		self.scwTableCase.add_with_viewport(self.Table)

	def UserSelectsNew(self, sender, tupleNumber):
		self.Highlighted = tupleNumber + 1
		self.Selected.set_text(self.TextView[tupleNumber + 1])

	def OKClicked(self, sender):
		if self.Highlighted != None:
			self.Window.hide()
			gtk.main_quit()

	def CancelClicked(self, sender):
		self.Highlighted = None
		self.Window.hide()
		gtk.main_quit()

if __name__ == '__main__':
	# Get an abstraction of the model's structure
	structure = ModelStructure()

	mainWindow = MainWindow(structure.Tables)
	alertWindow = AlertWindow()
	insert = Queries.InsertQuery()
	for wh in [mainWindow, alertWindow]:
		wh.Window.hide()


	while True:
		mainWindow.Window.show()
		gtk.main()
		mainWindow.Window.hide()
		if mainWindow.CurrentAction == Actions.Table['New']:
			newTableWindow = NewTableWindow(mainWindow.DesiredTable, structure.GetAttributesListByName(mainWindow.DesiredTable), structure)
			gtk.main()
			newTableWindow.Window.hide()
			print newTableWindow.SetAttributes
			if ((newTableWindow.CurrentAction == Actions.Table['New']) and
			   len([i for i in newTableWindow.SetAttributes if newTableWindow.SetAttributes[i] not in [None, '']]) != 0):
				try:
					insert.InsertFromDictionary(mainWindow.DesiredTable, newTableWindow.SetAttributes)
				except ImproperDataError as e:
					alertWindow.label.set_text(str(e))
	                                alertWindow.Window.show_all()
        	                        gtk.main()

			elif newTableWindow.CurrentAction == Actions.Table['New']:
				alertWindow.label.set_text('No data entered, nothing was saved.')
				alertWindow.Window.show_all()
				gtk.main()
		elif mainWindow.CurrentAction == Actions.Table['Edit']:
			print "Clicked Edit"
		elif mainWindow.CurrentAction == Actions.Table['Quit']:
			break
