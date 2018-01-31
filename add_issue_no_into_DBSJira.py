import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
# from time import sleep
# -*- coding: utf-8 -*-
__author__ = 'lizhangzhi'
'''
@file: add_issue_no_into_DBSJira.py
@time: 2018/1/31 15:26
'''


class IssuePage(object):
    login_user_name_loc = (By.ID, "login-form-username")
    login_user_password_loc = (By.ID, "login-form-password")
    login_button_loc = (By.ID, "login-form-submit")
    edit_button_loc = (By.ID, 'edit-issue')
    vendor_ticket_loc = (By.ID, "customfield_10946")
    vendor_ticket_value_loc = (By.ID, "customfield_10946-val")
    promotion_id_loc = (By.ID, "customfield_11204")
    promotion_id_value_loc = (By.ID, "customfield_11204-val")
    update_button_loc = (By.ID, "edit-issue-submit")

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.timeout = 30
        self.poll_frequency = 1

    # 重写元素定位方法
    def find_element(self, loc, clickable=False):
        try:
            if clickable:
                element = WebDriverWait(self.driver, self.timeout, self.poll_frequency)\
                    .until(ec.element_to_be_clickable(loc))
            else:
                element = WebDriverWait(self.driver, self.timeout, self.poll_frequency)\
                    .until(ec.visibility_of_element_located(loc))
            if element:
                return element
            else:
                elements = WebDriverWait(self.driver, self.timeout, self.poll_frequency)\
                    .until(ec.visibility_of_all_elements_located(loc))
                return elements[0] if elements else False
        except Exception:
            print("page {0} can't find locator {1}".format(self.driver.current_url, loc))

    def login(self, url, issue_no, user_name, user_password):
        self.driver.get(url+issue_no)
        self.find_element(self.login_user_name_loc).send_keys(user_name)
        self.find_element(self.login_user_password_loc).send_keys(user_password)
        self.find_element(self.login_button_loc, clickable=True).click()

    def add_issue_no(self, DBS_issue_no, ACI_issue_no):
        self.find_element(self.edit_button_loc, clickable=True).click()
        if re.match("AB", DBS_issue_no):
            self.find_element(self.vendor_ticket_loc).clear()
            self.find_element(self.vendor_ticket_loc).send_keys(ACI_issue_no)
            self.find_element(self.update_button_loc, clickable=True).click()
            vendor_ticket_value = self.find_element(self.vendor_ticket_value_loc).text
            try:
                assert vendor_ticket_value == ACI_issue_no
                print("Add issue %s into DBS jira %s successfully." % (ACI_issue_no, DBS_issue_no))
            except Exception as e:
                print("Add issue %s into DBS jira %s fail.Please to check" % (ACI_issue_no, DBS_issue_no))
                print(e)

        elif re.match("IDEA", DBS_issue_no):
            self.find_element(self.promotion_id_loc).clear()
            self.find_element(self.promotion_id_loc).send_keys(ACI_issue_no)
            self.find_element(self.update_button_loc, clickable=True).click()
            promotion_id_value = self.find_element(self.promotion_id_value_loc).text
            try:
                assert promotion_id_value == ACI_issue_no
                print("Add issue %s into DBS jira %s successfully." % (ACI_issue_no, DBS_issue_no))
            except Exception as e:
                print("Add issue %s into DBS jira %s fail.Please to check" % (ACI_issue_no, DBS_issue_no))
                print(e)

    def close_driver(self):
        self.driver.quit()

    def switch_to_other_issue(self, url, DBS_issue_no):
        self.driver.get(url + DBS_issue_no)

if __name__ == "__main__":
    user_name = "neilhe"
    user_password = "ideal3@pwd33"
    host = "https://116.12.252.147/"
    url = "dcifjira/browse/"
    issue = IssuePage()
    issue.login(host+url, "IDEAAA-40", user_name, user_password)
    with open("issue_add_to_DBSJira.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            DBS_issue_no = line.split(",")[0].strip("\n")
            ACI_issue_no = line.split(",")[1].strip("\n")
            issue.switch_to_other_issue(host+url, DBS_issue_no)
            issue.add_issue_no(DBS_issue_no, ACI_issue_no)
    issue.close_driver()
