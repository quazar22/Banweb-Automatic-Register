from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os#.path

i = 0
with open("user_info.txt", "r") as f:
    for x in f:
        if i == 0:
            UID = x.strip('\n')
            i += 1
            continue
        if i == 1:
            PIN = x.strip('\n')
            i += 1
            continue
        if i == 2:
            Apin = x.strip('\n')
            i += 1
            continue


driver = webdriver.Chrome()
driver.get("http://banweb7.nmt.edu/pls/PROD/twbkwbis.P_ValLogin")
sid = driver.find_element_by_name("sid")
pw = driver.find_element_by_name("PIN")

sid.send_keys(UID)
pw.send_keys(PIN)
pw.send_keys(Keys.RETURN)

driver.get("https://banweb7.nmt.edu/pls/PROD/twbkwbis.P_GenMenu?name=bmenu.P_StuMainMnu")
driver.get("https://banweb7.nmt.edu/pls/PROD/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu")
driver.get("https://banweb7.nmt.edu/pls/PROD/bwskfreg.P_AltPin")
submit = driver.find_element_by_xpath("//input[@type='submit'][@value='Submit']")
submit.send_keys(Keys.RETURN)

apin = driver.find_element_by_xpath("//input[@type='password'][@name='pin']")
apin.send_keys(Apin)
apin.send_keys(Keys.RETURN)

i = 1
html_id = "crn_id"
with open("crn_list.txt", "r") as f:
    for crn in f:
        crn = crn.strip('\n')
        crn_input = driver.find_element_by_id(html_id + str(i))
        crn_input.send_keys(crn)
        i += 1

submit = driver.find_element_by_xpath("//input[@type='submit'][@value='Submit Changes']")
submit.send_keys(Keys.RETURN)
