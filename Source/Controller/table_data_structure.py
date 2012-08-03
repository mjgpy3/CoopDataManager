#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Sun Jul 29 13:50:01 EDT 2012
# 
# 

class TableData:
    """
        An object representing data gathered from a table
    """
    def __init__(self, header, data):
        self.header = header
        self.data = data
        self.number_of_attributes = len(data[0])
        self.number_of_tuples = len(data)
