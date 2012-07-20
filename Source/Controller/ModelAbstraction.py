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

		#self.GetTableFromTuple(tables[0])

	def GetTableFromTuple(self, tableTuple):
		""" Returns a table object from the passed query tuple """
		assert tableTuple[0] == 'table'
		table = Table(tableTuple[1])
		data = tableTuple[-1]
		data = filter(lambda x: x[-1].replace('\n', '') in self.DataTypes ,map(lambda x: x.split(' '), data[data.index('(') + 1:data.index(')')].split(',')))
		table.Attributes =  map(lambda x: x[-2], data)
		return table
 

class Table:
	""" Represents a table """
	def __init__(self, name, attr = []):
		self.Name = name
		self.Attributes = attr

	def __repr__(self):
		return self.Name + ':' + ', '.join(self.Attributes)
		

a = ModelStructure()

a.FillTablesFromRawData()

for i in a.Tables:
	print i

print "TT:"

for i in a.TransactionTables:
	print i
