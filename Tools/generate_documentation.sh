#!/bin/bash

proj_path=~/Programming/MajorProjects/CoopManager

epydoc $proj_path/Source/View/*.py $proj_path/Source/Model/*.py $proj_path/Source/Controller/*.py -o $proj_path/Design/CodeDocumentation
