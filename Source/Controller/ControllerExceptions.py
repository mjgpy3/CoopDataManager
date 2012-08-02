#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Wed Aug  1 22:01:01 EDT 2012
# 
# 

class ImproperDataError(Exception):
	"""
		An exception raised when bad data is given in an SQL query.
	"""
	pass

class TableNotFoundError(Exception):
	"""
		An exception raised when a table is sought that does not exist.
	"""
	pass

class DatabaseNotFoundError(Exception):
	"""
		An exception raised when a database is sought that does not exist.
	"""
	pass
