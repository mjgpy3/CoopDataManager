#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Sat Jul 14 22:51:21 EDT 2012
# 
# 

import sqlite3, os, Schema

if raw_input('Are you sure you want to initialize the model?\nAll data will be lost (y/n): ')[0].lower() == 'y':
	if os.path.exists(Schema.ModelName):
		os.remove(Schema.ModelName)
else:
	print "Exiting"
	exit()

connectionToModel = sqlite3.connect(Schema.ModelName)

c = connectionToModel.cursor()

for query in Schema.TableCreationQueries:
	c.execute(query)
	connectionToModel.commit()

for query in Schema.TransactionTableQueries:
	c.execute(query)
	connectionToModel.commit()

c.close()
