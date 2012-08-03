#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Sat Jul 21 21:07:05 EDT 2012
# 
# 

import sys
sys.path.append('../Model')
import sqlite3

import schema
import model_abstraction
import table_data_structure
from controller_exceptions import *

class QueryObject:
    """
        The superclass for different queries that can be made. Essentially makes a connection to the database
        stated in the Schema.py file.
    """
    def __init__(self):
        self.query_text = ''
        try:
            open('../Model/' + schema.model_name, 'r')
        except IOError as e:
            raise DatabaseNotFoundError('Error while opening: ' + '../Model/' + schema.model_name)
 
        self.connection = sqlite3.connect('../Model/' + schema.model_name)
        self.cursor = self.connection.cursor()

        self.model_abstraction = model_abstraction.ModelStructure()

class InsertQuery(QueryObject):
    """
        A query object for inserting data into the model.
    """
    def __init__(self):
        QueryObject.__init__(self)

    def insert_from_dictionary(self, table_name, dictionary):
        dictionary = {key: value for key, value in dictionary.items() if value not in [None, '']}
        self.query_text, attributes, values  = "INSERT INTO " + table_name + " (", ', '.join(map(lambda x: "'" + str(x.name) + "'", dictionary)), ''
        abstract_attributes = self.model_abstraction.get_attributes_list_by_name(table_name)
        table = self.model_abstraction.get_table_by_name(table_name)
        for attr in dictionary:
            this_type = table.get_type_by_name(dictionary[attr])

            if attr.type == 'TEXT':
                dictionary[attr] = "'" + dictionary[attr] + "'"	

        self.query_text += attributes + ') VALUES (' + ', '.join(map(lambda key: str(dictionary[key]), dictionary)) + ');'

        try:
            self.cursor.execute(self.query_text)
        except sqlite3.OperationalError as e:
            raise ImproperDataError('Error with entry text: ' + str(e).split(' ')[-1])

        self.connection.commit()

class SelectQuery(QueryObject):
    """
        A query object for retriving data from the model.
    """
    def __init__(self):
        QueryObject.__init__(self)

    def get_all_data_from_table(self, table_name):
        """
            Returns all data from a passed table name
        """
        if table_name.lower() in map(lambda table: table.name.lower(), self.model_abstraction.tables):
            self.cursor.execute('SELECT ROWID, * FROM ' + table_name + ';')
        else:
            raise TableNotFoundError('Table "' + table_name + '" not in the model.' )

        return table_data_structure.TableData(['ROWID'] + self.model_abstraction.get_attributes_list_by_name(table_name), self.cursor.fetchall())
 
