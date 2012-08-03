#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Wed Jun 20 21:51:55 EDT 2012
# 
# 

""" This module contains the ConfigHandler class which is dedicated to handling the configuration for the framework """

class ConfigHandler:
    def __init__(self, config_name, config_defaults = {}):
        self.file_name = config_name
        if type({}) != type(config_defaults): raise TypeError('Default config information must be key value pairs')
        self.config = config_defaults

    def config_file_exists(self):
        try:
            a = open(self.file_name, 'r')
            a.close()
        except IOError:
            return False
        return True

    def parse_config(self):
        with open(self.file_name, 'r') as f:
            for line in f.read().split('\n'):
                if line != '': self.config[line.split('=')[0]] = line.split('=')[1]

    def update_config(self):
        with open(self.file_name, 'w') as f:
            for key in self.config:
                f.write(key + '=' + str(self.config[key]) + '\n')
