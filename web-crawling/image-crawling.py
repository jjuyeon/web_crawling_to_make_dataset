#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import json
import os
import urllib.request
import time
import timeit


# In[2]:


def get(maxcount, searchterm, folder):
    url = "https://www.google.co.in/search?q="+searchterm+"&source=lnms&tbm=isch"
    start = timeit.default_timer()  # 시작 시간 저장
    browser.get(url) # 브라우저 열기
    lastHeight = browser.execute_script("return document.body.scrollHeight")

    # 원하는 이미지 개수까지 얻을 수 있도록 스크롤을 내려줌
    counter = 0
    while True:
        counter = len(browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'))
        # scrolling을 하지 않는다면 한 페이지에 있는 이미지밖에 얻지 못함
        # execute_script함수 - 인자로 들어간 자바스크립트를 실행시켜주는 역할을 하는 함수
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 한번 내리는게 아니라 페이지의 맨 밑까지 내려주는 역할
        try:
            browser.find_element_by_id("smb").click() #'결과 더보기' 란 클릭 필요 없이 자동 넘어가는 기능
        except:
            pass
        time.sleep(2)
        newHeight = browser.execute_script("return document.body.scrollHeight")

        if (counter<=maxcount) and (lastHeight != newHeight):
            lastHeight = newHeight
            continue
        break
        
    # User-Agent를 통해 봇이 아닌 유저정보라는 것을 위해 사용
    header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"}    
    counter = 0    
    succounter = 0
    for x in browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'): # div태그에서 class name이 rg_meta인 것을 찾아온다
        if succounter >= maxcount:
            break
        
        counter = counter + 1        
        img = json.loads(x.get_attribute('innerHTML'))["ou"] # 이미지 url
        imgtype = 'jpg' # imgtype = json.loads(x.get_attribute('innerHTML'))["ity"], 이미지 확장자
        
        print ("Total Count:", counter)
        print ("Succsessful Count:", succounter)
        print ("URL:",img)
        
        try:  # 구글 이미지를 읽고 저장한다.
            req = urllib.request.Request(img, headers = header)
            raw_img = urllib.request.urlopen(req).read()
            File = open(os.path.join(folder , searchterm + "_" + str(succounter+1) + "." + imgtype), "wb")
            File.write(raw_img)
            File.close()
            succounter = succounter + 1
        except:
            print ("can't get img")
            
    print("--------------------------------------------------------")
    print (succounter, "succesfully downloaded")
    browser.close()
    stop = timeit.default_timer()
    print("**** Running time **** :", round((stop - start)/60, 6))  # 현재시각 - 시작시간 = 실행 시간(단위: 분)


# In[3]:


# firefox 브라우저 열기 위한 세팅
binary=FirefoxBinary('C:/Program Files/Mozilla Firefox/firefox.exe')
browser=webdriver.Firefox(executable_path='C:\\Users\Suyeon Jin\AppData\Local\Programs\Python\geckodriver.exe',firefox_binary=binary)


# In[4]:


searchterm = 'drone'
folder = 'Object-Detection'

if not os.path.exists(folder):
    os.mkdir(folder)

# 이미지 get(500장 수집)
maxcount = 500
get(maxcount, searchterm, folder)


# In[5]:


train = folder+'/train/'
if not os.path.exists(train):
    os.mkdir(train)

test = folder+'/test/'
if not os.path.exists(test):
    os.mkdir(test)


# In[9]:


# test/train 나누기
import shutil

for i in range (1,451):
    filename = searchterm+ "_" + str(i) + ".jpg"
    src = folder+'/'
    dir = train
    try:
        shutil.move(src+filename, dir+filename)
    except:
        print(filename,"이 존재하지 않음.")
        
for i in range(451,501):
    filename = searchterm+ "_" + str(i) + ".jpg"
    src = folder+'/'
    dir = test
    try:
        shutil.move(src+filename, dir+filename)
    except:
        print(filename,"이 존재하지 않음.")


# In[ ]:




