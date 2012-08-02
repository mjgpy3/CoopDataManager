#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Sat Jul 21 21:07:05 EDT 2012
# 
# 

import sys
sys.path.append('../Model')
import sqlite3
import Schema
import ModelAbstraction
import TableDataStructure
from ControllerExceptions import *

class QueryObject:
	"""
		The superclass for different queries that can be made. Essentially makes a connection to the database
		stated in the Schema.py file.
	"""
	def __init__(self):
                self.QueryString = ''
                try:
			open('../Model/' + Schema.ModelName, 'r')
		except IOError as e:
               		raise DatabaseNotFoundError('Error while opening: ' + '../Model/' + Schema.ModelName)
 
		self.Connection = sqlite3.connect('../Model/' + Schema.ModelName)
                self.Cursor = self.Connection.cursor()
   
		self.ModelAbstraction = ModelAbstraction.ModelStructure()

class InsertQuery(QueryObject):
	"""
		A query object for inserting data into the model.
	"""
	def __init__(self):
		QueryObject.__init__(self)

	def InsertFromDictionary(self, tableName, hashedValues):
		hashedValues = {key: value for key, value in hashedValues.items() if value not in [None, '']}
		self.QueryString, attributes, values  = "INSERT INTO " + tableName + " (", ', '.join(map(lambda x: "'" + str(x.Name) + "'", hashedValues)), ''
		abstractAttributes = self.ModelAbstraction.GetAttributesListByName(tableName)
		table = self.ModelAbstraction.GetTableByName(tableName)
		for attr in hashedValues:
			thisType = table.GetTypeByName(hashedValues[attr])
	
			if attr.Type == 'TEXT':
				hashedValues[attr] = "'" + hashedValues[attr] + "'"	

		self.QueryString += attributes + ') VALUES (' + ', '.join(map(lambda key: str(hashedValues[key]), hashedValues)) + ');'

		try:
			self.Cursor.execute(self.QueryString)
		except sqlite3.OperationalError as e:
			raise ImproperDataError('Error with entry text: ' + str(e).split(' ')[-1])

		self.Connection.commit()

class SelectQuery(QueryObject):
	"""
		A query object for retriving data from the model.
	"""
	def __init__(self):
		QueryObject.__init__(self)

	def GetAllDataFromTable(self, tableName):
		if tableName.lower() in map(lambda table: table.Name.lower(), self.ModelAbstraction.Tables):
			self.Cursor.execute('SELECT ROWID, * FROM ' + tableName + ';')
		else:
			raise TableNotFoundError('Table "' + tableName + '" not in the model.' )

		return TableDataStructure.TableData(['ROWID'] + self.ModelAbstraction.GetAttributesListByName(tableName), self.Cursor.fetchall())
 
