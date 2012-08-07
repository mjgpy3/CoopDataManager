#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Mon May  7 20:06:11 EDT 2012
# 
# 

import sys, unittest, hashlib
sys.path.append('../../Source/Controller')
import config_handler

from os import system as s

class testDataFormatters(unittest.TestCase):
    def setUp(self):
        self.file_name = 'test-config.cfg'
        self.being_tested = config_handler.ConfigHandler(self.file_name, {})

    def test_config_handler_returns_false_when_no_config_file_exists(self):
        self.assertFalse(self.being_tested.config_file_exists())

    def test_config_handler_returns_true_when_the_config_exists(self):
        s('touch ' + self.file_name)
        self.assertTrue(self.being_tested.config_file_exists())
	s('rm ' + self.file_name)

    def test_update_config_writes_an_expected_file(self):
        self.being_tested.config = {'attr1': 'value1', 'attr2': 'value2', 'attrN': 'valueN'}
        self.being_tested.update_config()
        with open(self.file_name, 'r') as f:
            md5_of_config_file = hashlib.md5()
            md5_of_config_file.update(f.read())
            md5_of_expected_text = hashlib.md5()
            md5_of_expected_text.update('attrN=valueN\nattr2=value2\nattr1=value1\n')
            self.assertEqual(md5_of_config_file.digest(), md5_of_expected_text.digest())
        s('rm ' + self.file_name)

    def tearDown(self):
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testDataFormatters))
    return suite

if __name__ == '__main__':
	unittest.TextTestRunner(verbosity=2).run(suite())
