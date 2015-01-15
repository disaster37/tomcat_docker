#!/usr/bin/python

import unittest
import os
import init

class InitTestCase(unittest.TestCase):
    """Tests for `init.py`."""

    @classmethod 
    def setUpClass(self):
      print("Settup unit test \n")
      init.TOMCAT_HOME = "/tmp/tomcat_docker"
      os.system("mkdir -p /tmp/tomcat_docker/conf")
      os.system("cp -R config/* /tmp/tomcat_docker/conf")

    @classmethod 
    def tearDownClass(self):
      print("TearDown unit test \n")
#      os.system("rm -rf /tmp/tomcat_docker")

    def test_do_setting_tomcat_user(self):
        """Check the function do_setting_tomcat_user"""
	self.assertRaises(Exception, init.do_setting_tomcat_user, None, None)
        init.do_setting_tomcat_user('user', 'password')

	file = open(init.TOMCAT_HOME +'/conf/tomcat-users.xml', 'r')
	self.assertNotRegexpMatches(file.read(), '{{TOMCAT_ADMIN_LOGIN}}', "The macro {{TOMCAT_ADMIN_LOGIN}} is not replace by value")
	self.assertNotRegexpMatches(file.read(), '{{TOMCAT_ADMIN_LOGIN}}', "The macro {{TOMCAT_ADMIN_PASSWORD}} is not replace by value")
	self.assertRegexpMatches(file.read(), '<user username="user" password="password" roles="tomcat"/>', "Problem when replace macr with value")
	file.close()

if __name__ == '__main__':
    unittest.main()
