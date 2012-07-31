#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Sun Jul 29 13:50:01 EDT 2012
# 
# 

class TableData:
	def __init__(self, header, data):
		self.Header = header
		self.Data = data
		self.NumberOfAttributes = len(data[0])
		self.NumberOfTuples = len(data)
