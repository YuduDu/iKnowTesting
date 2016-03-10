# -*- coding: utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import json

import time

from test import test

class Shop(test):
    __count =0

    def setUp(self):
        test.setUp(self)
        self.collection = self.db.get_collection("Shop")


    def tearDown(self):
        self.driver.close()

    def normal_login_Admin(self):
        data = {"userName":"admin","password":"111"}
        driver = self.driver
        driver.get("http://gene.rnet.missouri.edu/iKnow/Admin/login.php")
        assert "欢迎登录后台管理系统" in driver.title
        elem = driver.find_element_by_id("username")
        elem.send_keys(data["userName"])
        elem = driver.find_element_by_id("password")
        elem.send_keys(data["password"])
        elem.send_keys(Keys.RETURN)
        return driver

    def component_openframe(self,type):
        driver = self.driver
        driver.switch_to_frame('leftFrame')
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='header']/a[@href='index.html']")))
        driver.find_element_by_link_text("商家").click()
        if type == 'add':
            WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href = '../a_shop/ad_insert_shop.php']")))
            driver.find_element_by_xpath("//a[@href = '../a_shop/ad_insert_shop.php']").click()
        elif type == 'delete':
            driver.find_element_by_link_text('删除').click()

        driver.switch_to_default_content()
        return driver

    def component_add(self,driver,data):
        driver.switch_to_frame('rightFrame')
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "insert_shop")))
        driver.find_element_by_xpath("//input[@name ='name']").send_keys(data['name'])
        driver.find_element_by_xpath("//input[@name = 'password']").send_keys(data['password'])
        driver.find_element_by_xpath("//input[@name = 'phone']").send_keys(data['phone'])
        driver.find_element_by_xpath("//input[@name = 'province']").send_keys(data['province'])
        driver.find_element_by_xpath("//input[@name = 'city']").send_keys(data['city'])
        driver.find_element_by_xpath("//input[@name = 'address']").send_keys(data['address'])
        driver.find_element_by_xpath("//input[@name = 'email']").send_keys(data['email'])
        driver.find_element_by_xpath("//input[@name = 'pic']").clear()
        driver.find_element_by_xpath("//input[@name = 'pic']").send_keys(data['pic'])
        driver.find_element_by_xpath("//input[@name = 'opentime']").send_keys(data['start'])
        driver.find_element_by_xpath("//input[@name = 'closetime']").send_keys(data['end'])
        driver.find_element_by_xpath("//input[@name = 'submit']").click()
        driver.switch_to_default_content()
        return driver

    def test_01_sysAdmin_normal_addShop(self):
        self.driver = self.normal_login_Admin()
        datas = self.collection.find({"status":True})
        print "Testing sysAdmin add Shop function ..."
        print "data num: "+str(datas.count())
        for data in datas:
            #because the website can't redirect to insert form correctly after insert new shop, so have to redirect to insert form from left frame every time before insert.
            self.driver = self.component_openframe('add')
            self.driver = self.component_add(self.driver,data)
            alert = self.driver.switch_to_alert()
            try:
                assert '添加成功' in alert.text
            except:
                print "SysAdmin normal workflow: add Shop Failed ..\n"
                print "Expect Condition: 添加成功 in alert text."
                print "Alert text: "+ alert.text+".\n"
                print "Test data: \n"
                for key in data.keys():
                    print key+" : "+str(data[key])
                print '\n\n'
            alert.accept()

    def test_03_sysAdimin_incomplete_addShop(self):
        self.driver = self.normal_login_Admin()
        datas = self.collection.find({'status':False})
        print "Testing sysAdmin add Shop with incomplete information ..."
        print "data num: "+str(datas.count())
        for data in datas:
            #because the website can't redirect to insert form correctly after insert new shop, so have to redirect to insert form from left frame every time before insert.
            self.driver = self.component_openframe('add')
            self.driver = self.component_add(self.driver,data)
            alert =self.driver.switch_to_alert()
            try:
                assert '无法添加，请检查输入信息' in alert.text
            except:
                print "SysAdmin incomplete information add Shop Test Failed .."
                print "Expect Condition: 无法添加，请检查输入信息. in alert text."
                print "Alert text: "+ alert.text
                print "Test data:"
                for key in data.keys():
                    print key+" : "+str(data[key])
                print '\n\n'
            alert.accept()


    def test_02_sysAdmin_delete_shop(self):
        self.driver = self.normal_login_Admin()
        datas = self.collection.find({"status":True})
        print "Testing sysAdmin delete Shop function ..."
        driver = self.component_openframe('delete')
        driver.switch_to_frame('rightFrame')
        for data in datas:
            select = Select(driver.find_element_by_id('select_shop'))
            select.select_by_visible_text(data['name'])
            driver.find_element_by_id('submit').click()
            alert = driver.switch_to_alert()
            assert '您真的确定要删除吗？' in alert.text
            alert.accept()
            alert = driver.switch_to_alert()
            assert '删除成功' in alert.text
            alert.accept()







if __name__ == "__main__":
    unittest.main()