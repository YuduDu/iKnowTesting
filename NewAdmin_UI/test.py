# -*- coding: utf8 -*-
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import monogdb

class test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.db = monogdb.mongodb()
    def tearDown(self):
        self.driver.close()

