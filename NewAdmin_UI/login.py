# -*- coding: utf8 -*-
import unittest
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from test import test

class login (test):
    __count = 0

    def setUp(self):
        test.setUp(self)
        self.collection = self.db.get_collection("Login")

    def tearDown(self):
        self.driver.close()


    def loginTest(self):
        self.test_redirect_to_login()
        self.test_normal_login()
        self.test_invaild_information()
        self.test_blank_login()
        print "Test cases executed num: " + str(self.get_test_case_num())
        del self

    def component_test_step(self,data):
        driver = self.driver
        driver.get("http://gene.rnet.missouri.edu/iKnow/Admin/login.php")
        assert "欢迎登录后台管理系统" in driver.title
        elem = driver.find_element_by_id("username")
        elem.send_keys(data["userName"])
        elem = driver.find_element_by_id("password")
        elem.send_keys(data["password"])
        elem.send_keys(Keys.RETURN)
        return driver

    def test_normal_login(self):
        datas = self.collection.find({"status":True})
        print "Testing Normal login function with vaild information..."
        for data in datas:
            driver = self.component_test_step(data)
            try:
                assert "用户名或密码错误" not in driver.page_source
            except:
                print "Normal login function Testing FAILED! "
                print "Failed information: "
                print "         username:"+data["userName"]
                print "         password:"+data['password']+"\n"

            self.__count+=1
        print "Normal login function Testing Done.\n\n"

    def test_blank_login(self):
        datas = self.collection.find({"status":False,"testCaseNo":"1.4"})
        print "Testing login function with blank information..."
        for data in datas:
            driver = self.component_test_step(data)
            alert_txt = self.invaild_information_get_alert(driver)
            if not alert_txt:
                print "Blank Test FAILED!!"
                print "Failed information: Blank information logged in system"
                print "         url: "+driver.current_url
                print "         username: "+data["userName"]
                print "         password: "+data["password"]
                print "\n\n"
            else:
                try:
                    assert "请完整填写用户名和密码" in alert_txt
                except:
                    print "Blank Test FAILED!!"
                    print "Failed information: '请完整填写用户名和密码' not in alert txt"
                    print "         username: "+data["userName"]
                    print "         password: "+data["password"]
                    print "         alert txt: "+alert_txt
                    print "\n"


            self.__count+=1

        print "Blank information Login test is done.\n\n"

    def invaild_information_get_alert(self,driver):
            try:
                alert = driver.switch_to_alert()
                alert_txt = alert.text

            except:
                try:
                    assert "main" not in driver.current_url
                except:
                    return False

            else:
                alert.accept()
                return alert_txt


    def test_invaild_information(self):
        datas = self.collection.find({"status":False,"testCaseNo":"1.3"})
        print "Testing Login function with invaild information... "
        for data in datas:
            driver = self.component_test_step(data)
            alert_txt = self.invaild_information_get_alert(driver)
            if not alert_txt:
                print "Invaild information Test FAILED! "
                print "Failed information: invaild information logged in system"
                print "         url: "+ driver.current_url
                print "         username: "+data["userName"]
                print "         password: "+data["password"]
                print "\n"
            else:
                try:
                    assert "用户名或密码错误" in alert_txt
                except:
                    print "Login function Testing FAILED! "
                    print "Failed information: '用户名或密码错误' was not in alert text"
                    print "         username: "+data["userName"]
                    print "         password: "+data["password"]
                    print "         alert txt: "+alert_txt
                    print "\n"

            self.__count+=1

        print "Invaild information Login test is done.\n\n"

    def test_redirect_to_login(self):
        datas = self.collection.find({"testCaseNo":"1.2"})
        print "Testing redirect to login page... "
        for data in datas:
          self.driver.get(data['url'])

          try:
              alert = self.driver.switch_to_alert()
          except:
              print "Redirect to login page FAILED."
              print "URL: "+ data['url']
              print "No alert information poped!."

          alert_txt = alert.text
          try:
              assert "请登录" in alert_txt
          except:
              print "Redirect to login page FAILED."
              print "URL: "+ data['url']
              print "Alert didn't present right information. alert txt :" + alert_txt
              continue

          alert.accept()
          try:
            assert "欢迎进入iKnow管理系统" not in self.driver.title
          except:
            print "Redirect to login page FAILED."
            print "URL: "+ data['url']
            print "Get in main page!"
            continue
          self.__count+=1
        print "Redirect Testing Done. \n"

    def get_test_case_num(self):
        return self.__count;


    # def test_invaild_login(self):
    #     datas = self.collection.find({"status":False,"type":"invaild"})
    #     print "Testing Login function with invaild information: "
    #     for data in datas:
    #         driver = self.component_test_step(data)
    #         try:
    #             alert = driver.switch_to_alert()
    #             alert_txt = alert.text
    #
    #         except:
    #             try:
    #                 assert "main" not in driver.current_url()
    #             except:
    #                 print "Login function Testing FAILED! "
    #                 print "Failed information: invaild information loged in system"
    #                 print "         username: "+data["userName"]
    #                 print "         password: "+data["password"]
    #                 continue
    #             continue
    #
    #         try:
    #             assert "密码错误" in alert_txt
    #         except:
    #             print "Login function Testing FAILED! "
    #             print "Failed information: '密码错误' was not in alert text"
    #             print "         username: "+data["userName"]
    #             print "         password: "+data["password"]
    #
    #         alert.accept()
    #     print "Invaild information Login test is done."


#login1 = login()
#login1.loginTest();

if __name__ == "__main__":
    unittest.main()