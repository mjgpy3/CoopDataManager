#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Fri Jul 20 13:57:47 EDT 2012
# 
# 

def FormatCamelTableName(tableName):
	returnValue = tableName
	if 'Id' in returnValue:
		returnValue = returnValue.replace('Id', '')
	for i in range(len(returnValue) - 1, 0, -1): 
		if returnValue[i].isupper():
			returnValue = returnValue[:i] + ' ' + returnValue[i:]	

	return returnValue

