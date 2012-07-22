#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Thu Jul 19 19:59:08 EDT 2012
# 
# 

import sys
sys.path.append('../Model')
import sqlite3, Schema 


class ModelStructure:
	""" A class providing an abstraction on the sctucture of the model. """
	def __init__(self):
		try:
			self.Name = Schema.ModelName
		except:
			raise Exception('No model name in the Schema File')
		self.RawData = self.GetRawDataFromSqlite()
		self.Tables = []
		self.TransactionTables = []
		self.DataTypes = ['INTEGER', 'TEXT', 'REAL', 'BLOB']
		self.FillTablesFromRawData()

	def GetTableByName(self, tableName):
		for table in self.Tables:
			if table.Name == tableName:
				return table

	def GetAttributesListByName(self, tableName):
		""" 
			Tries to find the specified tableName. If it does, it will return a list of that table's attributes, if it
			does not it will return an empty list.
		"""
		for table in self.Tables:
			if table.Name.lower() == tableName.lower():
				return table.Attributes	
		return []	

	def GetRawDataFromSqlite(self):
		""" Returns all the header information for the passed table name by query. """
		connection = sqlite3.connect('../Model/' + self.Name)
		cursor = connection.cursor()
		cursor.execute('SELECT * FROM sqlite_master;')
		data = cursor.fetchall()
		cursor.close()
		return data

	def FillTablesFromRawData(self):
		""" After GetRawDataFromSqlite has been run, this method fills the values in the Tables property """
		allTables = []
		tables = []
		tTables = []
		indicies = []
		for line in self.RawData:
			if line[0] == 'table':
				allTables.append(line)
			elif line[0] == 'index':
				indicies.append(line[1])	

		tables = filter(lambda table: 'sqlite_autoindex_' + table[1] + '_1' not in indicies, allTables)
		tTables = filter(lambda table: 'sqlite_autoindex_' + table[1] + '_1' in indicies, allTables)
		
		for table in tables:
			self.Tables.append(self.GetTableFromTuple(table))
		for table in tTables:
			self.TransactionTables.append(self.GetTableFromTuple(table))

	def GetTableFromTuple(self, tableTuple):
		""" Returns a table object from the passed query tuple """
		assert tableTuple[0] == 'table'
		table = Table(tableTuple[1])
		data = tableTuple[-1]
		data = filter(lambda x: x[-1].replace('\n', '') in self.DataTypes ,map(lambda x: x.split(' '), data[data.index('(') + 1:data.index(')')].split(',')))
		table.Attributes =  []
		attr = map(lambda x: x[-2], data)
                types = map(lambda x: x[-1].strip('\n'), data)
		for i in range(len(data)):
			table.Attributes.append(Attribute(attr[i], types[i]))
		print table.Attributes
		return table
 

class Table:
	""" Represents a table """
	def __init__(self, name, attr = []):
		self.Name = name
		self.Attributes = attr

	def GetTypeByName(self, name):
		""" Returns the type of an attribute if its case sensitive name is found in the table's attributes. """
		for attribute in self.Attributes:
			if attribute.Name == name:
				return attribute.Type 

	def __repr__(self):
		return self.Name + ':' + ', '.join(map(lambda x: x.Name, self.Attributes))
		
class Attribute:
	""" Represents an attribute """
	def __init__(self, name, attrType):
		self.Name = name
		self.Type = attrType

	def __repr__(self):
		return self.Name + '('+ self.Type + ')'
