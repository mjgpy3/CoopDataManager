#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Wed Aug  1 22:01:01 EDT 2012
# 
# 

"""
    Defines exceptions specific to the controller.
"""

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

class NoModelInSchemaError(Exception):
    """
        An exception raised when the model name is not found in the schema file
    """
    pass
