#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Fri Jul 20 13:57:47 EDT 2012
# 
# 

def camel_to_readable(table_name, cut_id = True):
    return_value = table_name
    if 'Id' in return_value and cut_id:
        return_value = return_value.replace('Id', '')
    for i in range(len(return_value) - 1, 0, -1): 
        if return_value[i].isupper():
            return_value = return_value[:i] + ' ' + return_value[i:]	

    return return_value
