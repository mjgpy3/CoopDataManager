#!/bin/bash

shared_folder=~/Programming/MajorProjects/CoopManager/DevEnv/Shared/
source_folder=~/Programming/MajorProjects/CoopManager/Source

rm -r $shared_folder

cp -r $source_folder $shared_folder

for sub_dir in /View/ /Controller/ /Model/
do
  unix2dos $shared_folder$sub_dir*
done
