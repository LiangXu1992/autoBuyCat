# -*- coding: UTF-8 -*-
from selenium import webdriver
import simplejson as json
import datetime
import time
import traceback
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import os
import pdb
import ConfigParser
import sys
import codecs
import ast
import random

# public param
runningStatus = 'zheng chang'
jsonStr = []

cp = ConfigParser.SafeConfigParser()
with codecs.open('config.ini', 'r', encoding='utf-8') as f:
    cp.readfp(f)
username = cp.get(sys.argv[1], 'username')
passwd = cp.get(sys.argv[1], 'passwd')
myselfGoods = cp.get(sys.argv[1], 'myselfGoods')
shopGoodsUrl = cp.get('common_buy', 'shopGoodsUrl')
accountUrlList = []

def login(browser):
    # home page check id buyerIndex
    browser.get('http://www.jiaoyimao.com')
    if len(browser.find_elements_by_xpath("//*[@id='buyerIndex']")) != 0:
        return
    browser.get('https://api.open.uc.cn/cas/login?client_id=94')
    source=browser.find_element_by_xpath("//*[@id='nc_1_n1z']")
    ActionChains(browser).drag_and_drop_by_offset(source,1000,500).perform()
    time.sleep(2)
    source=browser.find_element_by_xpath("//*[@id='loginName']").send_keys(username)
    time.sleep(1)
    source=browser.find_element_by_xpath("//*[@id='password']").send_keys(passwd)
    time.sleep(1)
    source=browser.find_element_by_xpath("//*[@id='submit_btn']").click()
    global jsonStr
    jsonStr = []
    for cookie in browser.get_cookies():
        jsonStr.append({'name': cookie['name'],'value':cookie['value']})

def newBrowser():
    fireFoxOptions = webdriver.FirefoxOptions()
    # fireFoxOptions.set_headless()
    browser = webdriver.Firefox(firefox_options=fireFoxOptions)
    browser.get('https://www.jiaoyimao.com/')
    for cookie in jsonStr:
        browser.add_cookie({
            'domain': '.jiaoyimao.com',  # 此处xxx.com前，需要带点
            'name': cookie['name'],
            'value': cookie['value'],
            'path': '/'
        })
    login(browser)
    return browser

def buyGoods(browser):
    browser.get(random.sample(accountUrlList, 1)[0])
    # click buy button
    time.sleep(3)
    source = browser.find_element_by_xpath("//*[@id='buyNow']").click()
    # click understand,buy it
    time.sleep(5)
    if len(browser.find_elements_by_css_selector("[class='icon icon-dialog-close']")) == 1:
        time.sleep(3)
        source = browser.find_element_by_xpath("//*[@class='icon icon-dialog-close']").click()
    # click submit order
    time.sleep(3)
    source = browser.find_element_by_xpath("//*[@id='submitOrder']").click()
    # click submi pay
    pdb.set_trace()
    time.sleep(3)
    souce = browser.find_element_by_xpath("//*[@id='comfirmPayBtn']").click()
    time.sleep(10)
    browser.find_element_by_xpath("//*[@id='payPassword_rsainput']").send_keys('139260')
    time.sleep(3)
    browser.find_element_by_xpath("//*[@id='J_authSubmit']").click()
    pdb.set_trace()
    confirmGoods(browser)
    
def loopBuy(browser):
    while True:
        browser.get(random.sample(accountUrlList, 1)[0])
        # click buy button
        time.sleep(5)
        source = browser.find_element_by_xpath("//*[@id='buyNow']").click()
        # click understand,buy it
        time.sleep(3)
        if len(browser.find_elements_by_css_selector("[class='icon icon-dialog-close']")) == 1:
            time.sleep(3)
            source = browser.find_element_by_xpath("//*[@class='icon icon-dialog-close']").click()
            time.sleep(3)
        # click submit order
        if len(browser.find_elements_by_css_selector("[id='submitOrder']")) == 0:
            browser.get('https://my.alipay.com')
            time.sleep(60)
            continue
        source = browser.find_element_by_xpath("//*[@id='submitOrder']").click()
        time.sleep(3)
        
        if len(browser.find_elements_by_css_selector("[id='buttonRightAction']")) == 1:
            browser.find_element_by_xpath("//*[@id='buttonRightAction']").click()
            time.sleep(3)
            browser.get('https://my.alipay.com')
            time.sleep(60)
            continue
            
        if len(browser.find_elements_by_css_selector("[id='comfirmPayBtn']")) == 0:
            browser.get('https://my.alipay.com')
            time.sleep(60)
            continue
        souce = browser.find_element_by_xpath("//*[@id='comfirmPayBtn']").click()
        
        retryTimes = 0
        while True:
            retryTimes = retryTimes + 1
            if len(browser.find_elements_by_css_selector("[id='payPassword_rsainput']")) == 1:
                break
            else:
                if retryTimes == 5:
                    break
                time.sleep(1)
                continue
        if retryTimes == 5:
            retryTimes = 0
            continue
        browser.find_element_by_xpath("//*[@id='payPassword_rsainput']").send_keys('1')
        time.sleep(1.2)
        browser.find_element_by_xpath("//*[@id='payPassword_rsainput']").send_keys('3')
        time.sleep(1)
        browser.find_element_by_xpath("//*[@id='payPassword_rsainput']").send_keys('9')
        time.sleep(1.6)
        browser.find_element_by_xpath("//*[@id='payPassword_rsainput']").send_keys('2')
        time.sleep(1.4)
        browser.find_element_by_xpath("//*[@id='payPassword_rsainput']").send_keys('6')
        time.sleep(1.5)
        browser.find_element_by_xpath("//*[@id='payPassword_rsainput']").send_keys('0')
        time.sleep(2)
        browser.find_element_by_xpath("//*[@id='J_authSubmit']").click()
        time.sleep(60)
        confirmGoods(browser)

def confirmGoods(browser):
    try:
        browser.get(myselfGoods)
        time.sleep(2)
        browser.find_element_by_xpath("//*[@class='btn-buy-xs confirmReceiveBtn']").click()
        time.sleep(2)
        browser.find_element_by_xpath("//*[@id='buttonLeftAction']").click()
        time.sleep(10)
    except Exception, e:
        print e
        traceback.print_exc()
        
def getaccountUrlList(browser):
    i = 1
    global accountUrlList
    while True:
        browser.get(shopGoodsUrl + str(i))
        time.sleep(3)
        ll = browser.find_elements_by_xpath("//*[contains(text(), '163')]")
        if len(ll) == 0:
            break
        for v in ll:
            accountUrlList.append(v.get_attribute('href'))
        i = i + 1
        print i

browser = newBrowser()
getaccountUrlList(browser)
buyGoods(browser)
loopBuy(browser)