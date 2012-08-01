#!/usr/bin/env python
import sys
sys.path.append('../Controller')
from ModelAbstraction import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade    
import ViewBrain, Actions, Queries

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
		if self.cmbSelectedTable.get_active() != 0:
			self.CurrentAction = Actions.Table['New']
		else:
			self.CurrentAction = None
		gtk.main_quit()

class NewTableWindow:
	def __init__(self, tableName, attributes):
		self.SetAttributes = {}
		self.CurrentAction = Actions.Table['None']
		self.TableName = tableName

		# Handle the window itself
		self.GladeFile = 'NewEntry.glade'
		self.wTree = gtk.glade.XML(self.GladeFile)
                self.Window = self.wTree.get_widget('wdwNewEntry')
		self.Window.set_title('Add New ' + tableName)
		self.Window.set_resizable(False)
		self.Window.connect('destroy', lambda x: gtk.main_quit())
		self.SelectIdWindow = SelectIdWindow()

		# Create the master Vertical Box
		self.MasterVBox = gtk.VBox()
		for attribute in attributes:
			hbox = gtk.HBox()
			label = gtk.Label()
			entry = gtk.Entry()
			label.set_text(ViewBrain.FormatCamelTableName(attribute.Name) + ':')
			hbox.add(label)
                       	hbox.add(entry)

			if 'Id' in attribute.Name:
				button = gtk.Button('Browse')
				button.connect('clicked', self.UserSelectsBrowse, attribute.Name, entry)
				entry.set_editable(False)
				hbox.add(button)
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

	def UserSelectsBrowse(self, sender, tableName, entry):
		print "Browsing for " + tableName
		table_data = None #Queries.SelectQuery().GetAllDataFromTable('')
		model_structure = ModelStructure()

		#for table in model_structure.Tables:
			#if table.Name.lower() in :
		#		print table
		#		print tableName
		#		print '-----> ' + table.References[str(tableName)]
		table_data = Queries.SelectQuery().GetAllDataFromTable(model_structure.GetTableByName(self.TableName).References[str(tableName)]) 
		#		break
		self.SelectIdWindow.AddTableData(table_data)
		self.SelectIdWindow.Window.show_all()
		gtk.main()
		print 'Past there'
		self.SetAttributes[model_structure.GetAttributeFromTable(tableName, self.TableName)] = self.SelectIdWindow.Highlighted
		if self.SelectIdWindow.Highlighted != None:
			entry.set_text(str(self.SelectIdWindow.Highlighted))

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

class SelectIdWindow:
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
		self.Table = gtk.Table(0, 0, False)#tableData.NumberOfAttributes - 1, tableData.NumberOfTuples + 1, True)

		for index in range(tableData.NumberOfAttributes):
			button = gtk.Button(str(ViewBrain.FormatCamelTableName(str(tableData.Header[index]))))
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
		self.Highlighted == None
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
			newTableWindow = NewTableWindow(mainWindow.DesiredTable, structure.GetAttributesListByName(mainWindow.DesiredTable))
			gtk.main()
			newTableWindow.Window.hide()
			if newTableWindow.CurrentAction == Actions.Table['New']:
				insert.InsertFromDictionary(mainWindow.DesiredTable, newTableWindow.SetAttributes)
		elif mainWindow.CurrentAction == Actions.Table['Edit']:
			print "Clicked Edit"
		elif mainWindow.CurrentAction == Actions.Table['Quit']:
			break
