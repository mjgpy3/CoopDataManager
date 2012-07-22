#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Sat Jul 21 21:07:05 EDT 2012
# 
# 

import sys
sys.path.append('../Model')
import sqlite3, Schema, ModelAbstraction

class InsertQuery:
	def __init__(self):
		self.QueryString = ''
		try:
			self.Connection = sqlite3.connect('../Model/' + Schema.ModelName )
			self.Cursor = self.Connection.cursor()
		except:		# POKEMON Exception handling!!!
			raise Exception('Failed to connect to the model!')
		self.ModelAbstraction = ModelAbstraction.ModelStructure()

	def InsertFromDictionary(self, tableName, hashedValues):
		self.QueryString, attributes, values  = "INSERT INTO " + tableName + " (", ', '.join(map(lambda x: "'" + str(x.Name) + "'", hashedValues)), ''
		abstractAttributes = self.ModelAbstraction.GetAttributesListByName(tableName)
		table = self.ModelAbstraction.GetTableByName(tableName)
		for attr in hashedValues:
			thisType = table.GetTypeByName(hashedValues[attr])
			
			print hashedValues[attr], attr, thisType		
	
			if attr.Type == 'TEXT':
				hashedValues[attr] = "'" + hashedValues[attr] + "'"	

		self.QueryString += attributes + ') VALUES (' + ', '.join(map(lambda key: hashedValues[key], hashedValues)) + ');'

		print self.QueryString

		self.Cursor.execute(self.QueryString)
		self.Connection.commit()
