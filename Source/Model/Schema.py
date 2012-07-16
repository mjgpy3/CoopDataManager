#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Sat Jul 14 22:47:42 EDT 2012
# 
#

ModelName = 'test'

TableCreationQueries = ["""
CREATE TABLE Semester(
  BeginDate TEXT,
  EndDate TEXT
);
""", """
CREATE TABLE Address(
  Line1 TEXT,
  Line2 TEXT,
  City TEXT,
  State TEXT,
  Zip INTEGER 
);
""", """
CREATE TABLE Parent(
  LastName TEXT,
  FirstName TEXT,
  Phone1 INTEGER,
  Phone2 INTEGER,
  Email TEXT,
  AddressId INTEGER,
  FOREIGN KEY(AddressId) REFERENCES Address(ROWID)
);
""", """
CREATE TABLE Student(
  LastName TEXT,
  FirstName TEXT,
  Parent1Id INTEGER,
  Parent2Id INTEGER,
  Grade TEXT,
  FOREIGN KEY(Parent1Id) REFERENCES Parent(ROWID),
  FOREIGN KEY(Parent2ID) REFERENCES Parent(ROWID)
);
""", """
CREATE TABLE Class(
  Room TEXT,
  Time TEXT,
  Cost REAL,
  SemesterId INTEGER,
  FOREIGN KEY(SemesterId) REFERENCES Semester(ROWID)
);
"""]

TransactionTableQueries = ["""
CREATE TABLE IsEnrolledIn(
  StudentId INTEGER,
  ClassId INTEGER,
  PRIMARY KEY(StudentId, ClassId),
  FOREIGN KEY(StudentID) REFERENCES Student(ROWID),
  FOREIGN KEY(ClassId) REFERENCES Class(ROWID)
);
""", """
CREATE TABLE Teaches(
  ParentId INTEGER,
  ClassId INTEGER,
  PRIMARY KEY(ParentId, ClassId),
  FOREIGN KEY(ParentId) REFERENCES Parent(ROWID),
  FOREIGN KEY(ClassId) REFERENCES Class(ROWID)
);
"""]
