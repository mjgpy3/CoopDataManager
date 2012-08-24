#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Sun Jul 29 13:50:01 EDT 2012
# 
# 

"""
    Contains the TableData class which is used to represent data when it is returned from the model
"""

class TableData:
    """
        An object representing data gathered from a table
    """
    def __init__(self, header, data):
        self.header = header
        self.data = data
        if data != []:
            self.number_of_attributes = len(data[0])
        else:
            self.number_of_attributes = None
        self.number_of_tuples = len(data)
