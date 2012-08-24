#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Sat Jul 14 22:51:21 EDT 2012
# 
# 

"""
    This file uses the model structure found in the schema.py file to generate a ModelStructure, and then it
    generates the database for the model due to the ModelStructure and schema
"""

import sqlite3, os, schema
import model_abs

a = model_abs.ModelStructure()
a.build_from_schema()

if raw_input('Are you sure you want to initialize the model?\nAll data will be lost (y/n): ')[0].lower() == 'y':
    if os.path.exists(a.name):
        os.remove(a.name)
    else:
        print "Exiting"
        exit()

connection_to_model = sqlite3.connect(a.name)

cursor = connection_to_model.cursor()

for table in a.tables + a.transaction_tables:
    print table.get_generation_statement()
    cursor.execute(table.get_generation_statement())
    connection_to_model.commit()

