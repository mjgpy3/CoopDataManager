#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Thu Jul 19 19:59:08 EDT 2012
# 
# 

import sys
sys.path.append('../Model')
import sqlite3 
import schema 
from controller_exceptions import *

class ModelStructure:
    """ 
        A class providing an abstraction on the sctucture of the model. 
    """
    def __init__(self):
        try:
            self.name = schema.model_name
        except:
            raise NoModelInSchemaError('No model name in the Schema File')
        self.raw_data = self.get_raw_data_from_sqlite()
        self.tables = []
        self.transaction_tables = []
        self.data_types = ['INTEGER', 'TEXT', 'REAL', 'BLOB']
        self.fill_tables_from_raw_data()

    def get_table_by_name(self, table_name):
        """
            Returns a table with the passed, case-sensitive name
        """
        for table in self.tables + self.transaction_tables:
            if table.name == table_name:
                return table

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
            if type(table) != type(None):
                if table.name.lower() == table_name.lower():
                    return table.attributes	

        return []	

    def get_raw_data_from_sqlite(self):
        """ 
            Returns all the header information for the passed table name by query. 
        """
        connection = sqlite3.connect('../Model/' + self.name)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM sqlite_master;')
        data = cursor.fetchall()
        cursor.close()
        return data

    def fill_tables_from_raw_data(self):
        """ 
            After GetRawDataFromSqlite has been run, this method fills the values in the Tables property 
        """
        all_tables = []
        tables = []
        t_tables = []
        indicies = []
        for line in self.raw_data:
            if line[0] == 'table':
                all_tables.append(line)
            elif line[0] == 'index':
                indicies.append(line[1])	

        # Filter out the transaction tables and the normal tables
        tables = filter(lambda table: 'sqlite_autoindex_' + table[1] + '_1' not in indicies, all_tables)
        t_tables = filter(lambda table: 'sqlite_autoindex_' + table[1] + '_1' in indicies, all_tables)

        for table in tables:
            self.tables.append(self.get_table_from_tuple(table))
        for table in t_tables:
            self.transaction_tables.append(self.get_table_from_tuple(table))

    def get_table_from_tuple(self, table_tuple):
        """ 
            Returns a table object from the passed query tuple 
        """
        assert table_tuple[0] == 'table'
        table = Table(table_tuple[1])
        data = table_tuple[-1]
        data = filter(lambda x: x[-1].replace('\n', '') in self.data_types ,map(lambda x: x.split(' '), data[data.index('(') + 1:data.index(')')].split(',')))
        table.attributes =  []
        attr = map(lambda x: x[-2], data)
        types = map(lambda x: x[-1].strip('\n'), data)
        for i in range(len(data)):
            table.attributes.append(Attribute(attr[i], types[i]))
        table.references = self.get_reference_dictionary(table_tuple[-1])
        return table

    def get_reference_dictionary(self, schema_line):
        """
            Looks through a line of the schema and generates a dictionary of references of the form:
            key: value = attributeInTable: attributeItRefersTo.
        """
        get_attribute = lambda attr: attr[attr.index('(') + 1:attr.index(')')]
        get_referee =  lambda attr: attr[:attr.index('(')]
        words = schema_line.split(' ')
        raw = [(words[i-1], words[i+1]) for i in range(len(words)) if 'references' in words[i].lower()]
        dictionary = {}
        for index in range(len(raw)):
            dictionary[get_attribute(raw[index][0])] = get_referee(raw[index][1])

        return dictionary
 

class Table:
    """ 
        Represents a table 
    """
    def __init__(self, name, attr = []):
        self.name = name
        self.attributes = attr
        self.references = None

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
    def __init__(self, name, type_):
        self.name = name
        self.type = type_

    def __repr__(self):
        return self.name
