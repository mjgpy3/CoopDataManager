#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Wed Aug 22 10:23:53 EDT 2012
# 
# 

import sys
sys.path.append('../Controller')
import sqlite3
import schema
import schem
from controller_exceptions import *

class ModelStructure:
    """ 
        A class providing an abstraction on the sctucture of the model. 
    """
    name = ''
    tables = []
    transaction_tables = []

    def get_table_by_name(self, table_name):
        """
            Returns a table with the passed, case-sensitive name
        """
        for table in self.tables + self.transaction_tables:
            if table.name == table_name:
                return table

    def build_from_schema(self):
        schem.build_model_structure(self)

    def get_attribute_from_table(self, attribute_name, table_name):
        """
            Returns an attribute by the passed attribute name from the passed table name
        """
        return self.get_table_by_name(table_name).get_attribute_by_name(attribute_name)

    def get_attributes_list_by_name(self, table_name):
        """ 
            Tries to find the specified tableName. If it does, it will return a list of that table's attributes, if it
            does not it will return an empty list.
        """
        for table in self.tables + self.transaction_tables:
            if table.name.lower() == table_name.lower():
                return table.attributes

        return []


class Table:
    """ 
        Represents a table 
    """
    def __init__(self, name, attr = [], primary_key = []):
        self.name = name
        self.attributes = attr
        self.references = {}
        self.primary_key = None

    def get_generation_statement(self):
        statement = 'CREATE TABLE ' + self.name + '(\n'
        for attr in self.attributes[:-1]:
            statement += '  ' + attr.name + ' ' + attr.type + ',\n'
        statement += '  ' + self.attributes[-1].name + ' ' + self.attributes[-1].type

        if self.primary_key != None:
            statement += ',\n  PRIMARY KEY(' + ','.join([i.name for i in self.primary_key]) + ')'

        if self.references != {}:
            for key in self.references:
                statement += ',\n  FOREIGN KEY(' + key + ') REFERENCES ' + self.references[key] + '(ROWID)'

        return statement + '\n);'

    def set_reference(self, attribute, table):
        if self.references == None: self.references = {}
        self.references[attribute.name] = table.name

    def get_attribute_by_name(self, name):
        """
            Returns an attribute in the table if its case sensitive name is found.
        """
        for attribute in self.attributes:
            if attribute.name == name:
                return attribute

    def get_type_by_name(self, name):
        """ 
            Returns the type of an attribute if its case sensitive name is found in the table's attributes. 
        """
        for attribute in self.attributes:
            if attribute.name == name:
                return attribute.type

    def __repr__(self):
        return self.name + ':' + ', '.join([x.name for x in self.attributes])

class Attribute:
    """ 
        Represents an attribute 
    """
    def __init__(self, name, type_, acceptable_values = None):
        self.name = name
        assert type_ in ['INTEGER', 'TEXT', 'REAL', 'BLOB']
        self.type = type_.upper()
        self.acceptable_values = acceptable_values

    def __repr__(self):
        return self.name

