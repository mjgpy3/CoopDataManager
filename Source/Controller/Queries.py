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

class QueryObject:
	def __init__(self):
                self.QueryString = ''
                try:
                        self.Connection = sqlite3.connect('../Model/' + Schema.ModelName )
                        self.Cursor = self.Connection.cursor()
                except:         # POKEMON Exception handling!!!
                        raise Exception('Failed to connect to the model!')
                self.ModelAbstraction = ModelAbstraction.ModelStructure()

class InsertQuery(QueryObject):
	def __init__(self):
		QueryObject.__init__(self)

	def InsertFromDictionary(self, tableName, hashedValues):
	#	for key in hashedValues:
	#		if hashedValues[key] == None:
	#			del hashedValues[key]
		hashedValues = {key: value for key, value in hashedValues.items() if value not in [None, '']}
		print hashedValues
		self.QueryString, attributes, values  = "INSERT INTO " + tableName + " (", ', '.join(map(lambda x: "'" + str(x.Name) + "'", hashedValues)), ''
		abstractAttributes = self.ModelAbstraction.GetAttributesListByName(tableName)
		table = self.ModelAbstraction.GetTableByName(tableName)
		for attr in hashedValues:
			thisType = table.GetTypeByName(hashedValues[attr])
			
			print hashedValues[attr], ': ' + str(attr), thisType		
	
			if attr.Type == 'TEXT':
				hashedValues[attr] = "'" + hashedValues[attr] + "'"	

		self.QueryString += attributes + ') VALUES (' + ', '.join(map(lambda key: hashedValues[key], hashedValues)) + ');'

		print self.QueryString

		self.Cursor.execute(self.QueryString)
		self.Connection.commit()

class SelectQuery(QueryObject):
	def __init__(self):
		QueryObject.__init__(self)

	def GetAllDataFromTable(self, tableName):
		if tableName.lower() in map(lambda table: table.Name.lower(), self.ModelAbstraction.Tables):
			self.Cursor.execute('SELECT ROWID, * FROM ' + tableName + ';')
		else:
			raise Exception('Table "' + tableName + '" not in the model.' )

		return TableDataStructure.TableData(['ROWID'] + self.ModelAbstraction.GetAttributesListByName(tableName), self.Cursor.fetchall())
