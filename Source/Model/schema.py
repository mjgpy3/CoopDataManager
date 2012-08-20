#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Sat Jul 14 22:47:42 EDT 2012
# 
#

model_name = 'test.db'

# A list of queries that will generate general entity/noun type tables
table_creation_queries = ["""
CREATE TABLE Semester(
  FallOrSpring TEXT,
  Year INTEGER
);
""", """
CREATE TABLE Parent(
  LastName TEXT,
  FirstName TEXT
);
""", """
CREATE TABLE Student(
  LastName TEXT,
  FirstName TEXT,
  Parent1Id INTEGER,
  Parent2Id INTEGER,
  Grade TEXT,
  FOREIGN KEY(Parent1Id) REFERENCES Parent(ROWID),
  FOREIGN KEY(Parent2Id) REFERENCES Parent(ROWID)
);
""", """
CREATE TABLE Class(
  Name TEXT,
  Hour TEXT,
  Cost INTEGER,
  AgeMin TEXT,
  AgeMax TEXT,
  MaxNumberOfStudents INTEGER,
  SemesterId INTEGER,
  FOREIGN KEY(SemesterId) REFERENCES Semester(ROWID)
);
"""]

# A list of queries that will generate tables that are transaction/link tables
transaction_table_queries = ["""
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
""", """
CREATE TABLE IsAHelperFor(
  ParentId INTEGER,
  ClassId INTEGER,
  PRIMARY KEY(ParentId, ClassId),
  FOREIGN KEY(ParentId) REFERENCES Parent(ROWID),
  FOREIGN KEY(ClassId) REFERENCES Class(ROWID)
);
""", """
CREATE TABLE TakesPlaceDuring(
  ClassId INTEGER,
  SemesterId INTEGER,
  PRIMARY KEY(ClassId, SemesterId),
  FOREIGN KEY(ClassId) REFERENCES Class(ROWID),
  FOREIGN KEY(SemesterId) REFERENCES Semester(ROWID)
);
"""]
