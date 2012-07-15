#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Sat Jul 14 23:45:12 EDT 2012
# 
# 

import Schema, sqlite3

connectionToModel = sqlite3.connect(Schema.ModelName)

c = connectionToModel.cursor()


Inserts = ["INSERT INTO Semester ('BeginDate', 'EndDate') VALUES ('2012-01-01', '2012-05-07');", \
	   "INSERT INTO Semester ('BeginDate', 'EndDate') VALUES ('2012-08-01', '2012-12-17');", \
           "INSERT INTO Address ('Line1', 'City', 'State', 'Zip') VALUES ('124 Magic St.', 'Magic City', 'MS', 12345);", \
	   "INSERT INTO Address ('Line1', 'Line2', 'City', 'State', 'Zip') VALUES ('43 Burger Ave.', 'Apt. 5','Fry Ville', 'BS', 98724);", \
	   "INSERT INTO Address ('Line1', 'City', 'State', 'Zip') VALUES ('01 Video Game Ln.', 'Sim City', 'GS', 12345);", \
	   "INSERT INTO Address ('Line1', 'City', 'State', 'Zip') VALUES ('911 Bogus blvd.', 'Alias City', 'FS', 82934);", \
	   "INSERT INTO Address ('Line1', 'City', 'State', 'Zip') VALUES ('909 Skate Parkway.', 'Skatetown USA', 'SS', 20872);", \
	   "INSERT INTO Parent ('LastName', 'FirstName', 'Phone1', 'Email', 'AddressId') VALUES ('Doe', 'John', 9384736475, 'fake@fake.com' , 1);", \
	   "INSERT INTO Parent ('LastName', 'FirstName', 'Phone1', 'Email', 'AddressId') VALUES ('Doe', 'Jane', 9384736475, 'fake@other.com', 1);", \
	   "INSERT INTO Parent ('LastName', 'FirstName', 'Phone1', 'Email', 'AddressId') VALUES ('Smith', 'Jack', 918394029, 'cooleo@someplace.com', 2);", \
	   "INSERT INTO Parent ('LastName', 'FirstName', 'Phone1', 'Email', 'AddressId') VALUES ('Weasley', 'Ronald', 9832457653, 'magicman@hogwarts.com', 4);", \
	   "INSERT INTO Parent ('LastName', 'FirstName', 'Phone1', 'Email', 'AddressId') VALUES ('Krueger', 'Freddy', 193849283, 'crazy@hi.com', 3);", \
	   "INSERT INTO Student ('LastName', 'FirstName', 'Parent1Id', 'Parent2Id', 'Grade') VALUES ('Doe', 'Jimmy', 1, 2, '1st');"]



#"insert into t1 (data,num) values ('This is sample data',3);"
"""
CREATE TABLE Student(
  LastName TEXT,
  FirstName TEXT,
  Parent1Id INTEGER,
  Parent2Id INTEGER,
  Grade TEXT,
  FOREIGN KEY(Parent1Id) REFERENCES Parent(ROWID),
  FOREIGN KEY(Parent2ID) REFERENCES Parent(ROWID)
);
"""

for insert in Inserts:
	c.execute(insert)
	connectionToModel.commit()

c.close()

