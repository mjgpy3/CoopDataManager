#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Sat Jul 21 21:07:05 EDT 2012
# 
# 

import sys
sys.path.append('../Model')
import sqlite3, Schema

class InsertQuery:
	def __init__(self):
		self.QueryString = ''
		try:
			self.Connection = sqlite3.connect('../Model/' + Schema.ModelName )
			self.cursor = self.Connection.cursor()
		except:		# POKEMON!!!
			raise Exception('Failed to connect to the model!')


connection = sqlite3.connect('../Model/' + self.Name)
                cursor = connection.cursor()



	def InsertFromDictionary(self, tableName, hashedValues):
		
