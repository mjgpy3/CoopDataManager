#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Sat Jul 14 22:47:42 EDT 2012
# 
#

ModelName = 'test.db'

TableCreationQueries = ["""
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
  Cost REAL,
  AgeMin INTEGER,
  AgeMax INTEGER,
  MaxNumberOfStudents INTEGER,
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
