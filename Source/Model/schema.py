#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Wed Aug 22 10:32:15 EDT 2012
# 
# 

import model_abstraction as m

def build_model_structure(model_structure):
    tables = []
    transaction_tables = []
    name = 'test2.db'

    # Semester Attributes
    fall_or_spring_FOS = m.Attribute('FallOrSpring', 'TEXT', ['Fall', 'Spring'])
    year_FOS = m.Attribute('Year', 'INTEGER')

    # Semester Table 
    semester_table = m.Table('Semester', [fall_or_spring_FOS, year_FOS])
    semester_table.primary_key = [fall_or_spring_FOS, year_FOS]
    tables.append(semester_table)


    # Parent Attributes
    last_name_P = m.Attribute('LastName', 'TEXT')
    first_name_P = m.Attribute('FirstName', 'TEXT')

    # Parent Table
    parent_table = m.Table('Parent', [last_name_P, first_name_P])
    parent_table.primary_key = [last_name_P, first_name_P]
    tables.append(parent_table)


    # Student Attributes
    last_name_S = m.Attribute('LastName', 'TEXT')
    first_name_S = m.Attribute('FirstName', 'TEXT')
    parent_id_1_S = m.Attribute('Parent1Id', 'INTEGER')
    parent_id_2_S = m.Attribute('Parent2Id', 'INTEGER')
    grade_S = m.Attribute('Grade', 'TEXT')
    
    # Student Table
    student_table = m.Table('Student', [last_name_S, first_name_S, parent_id_1_S, parent_id_2_S, grade_S])
    student_table.primary_key = [last_name_S, first_name_S]
    student_table.set_reference(parent_id_1_S, parent_table)
    student_table.set_reference(parent_id_2_S, parent_table)
    tables.append(student_table)


    # Class Attributes
    name_C = m.Attribute('Name', 'TEXT')
    hour_C = m.Attribute('Hour', 'TEXT')
    cost_C = m.Attribute('Cost', 'INTEGER')
    grade_min_C = m.Attribute('GradeMin', 'TEXT', ['Nurs', 'Pre-K', 'K', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
    grade_max_C = m.Attribute('GradeMax', 'TEXT', ['Nurs', 'Pre-K', 'K', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
    max_number_of_students_C = m.Attribute('MaxNumberOfStudents', 'INTEGER')
    semester_id_C = m.Attribute('SemesterId', 'INTEGER')

    # Class Table
    class_table = m.Table('Class', [name_C, hour_C, cost_C, grade_min_C, grade_max_C, max_number_of_students_C, semester_id_C])
    class_table.primary_key = [name_C, semester_id_C]
    class_table.set_reference(semester_id_C, semester_table)
    tables.append(class_table)


    # IsEnrolledIn Attributes
    student_id_I = m.Attribute('StudentId', 'INTEGER')
    class_id_I = m.Attribute('ClassId', 'INTEGER')

    # IsEnrolledIn Table
    is_enrolled_in_table = m.Table('Enrollment', [student_id_I, class_id_I])
    is_enrolled_in_table.primary_key = [student_id_I, class_id_I]
    is_enrolled_in_table.set_reference(student_id_I, student_table)
    is_enrolled_in_table.set_reference(class_id_I, class_table)
    transaction_tables.append(is_enrolled_in_table)

  
    # Teaches Attributes
    parent_id_T = m.Attribute('ParentId', 'INTEGER')
    class_id_T = m.Attribute('ClassId', 'INTEGER')

    # Teaches Table
    teaches_table = m.Table('Teacher', [parent_id_T, class_id_T])
    teaches_table.primary_key = [parent_id_T, class_id_T]
    teaches_table.set_reference(parent_id_T, parent_table)
    teaches_table.set_reference(class_id_T, class_table)
    transaction_tables.append(teaches_table)


    # IsHelperFor Attributes
    parent_id_IHF = m.Attribute('ParentId', 'INTEGER')
    class_id_IHF = m.Attribute('ClassId', 'INTEGER')

    # Teaches Table
    is_helper_for_table = m.Table('Helper', [parent_id_IHF, class_id_IHF])
    is_helper_for_table.primary_key = [parent_id_IHF, class_id_IHF]
    is_helper_for_table.set_reference(parent_id_IHF, parent_table)
    is_helper_for_table.set_reference(class_id_IHF, class_table)
    transaction_tables.append(is_helper_for_table)

    # Generate Structure
    model_structure.name = name
    model_structure.tables = tables
    model_structure.transaction_tables = transaction_tables
    return model_structure
