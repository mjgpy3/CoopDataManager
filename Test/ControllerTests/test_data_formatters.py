#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Mon May  7 20:06:11 EDT 2012
# 
# 

import sys, unittest
sys.path.append('../../Source/Controller')
import data_formatters

from os import system as s

class testDataFormatters(unittest.TestCase):
    def setUp(self):
        pass

    def test_data_formatters_performs_as_expected_for_a_given_set_of_data(self):
        self.assertEqual(data_formatters.camel_to_readable('TableName'), 'Table Name')
        self.assertEqual(data_formatters.camel_to_readable('TableNameOrId', False), 'Table Name Or Id')
        self.assertEqual(data_formatters.camel_to_readable('TableNameOrId', True), 'Table Name Or')
        self.assertEqual(data_formatters.camel_to_readable('Foo'), 'Foo')

    def tearDown(self):
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testDataFormatters))
    return suite

if __name__ == '__main__':
	unittest.TextTestRunner(verbosity=2).run(suite())
