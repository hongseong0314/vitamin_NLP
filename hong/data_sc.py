from selenium import webdriver
from bs4 import BeautifulSoup
import lxml
import time
import numpy as np
import pandas as pd
import requests
import os
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def yogiyo_scrapping(*ar):
    """
    가게 이름을 받아서 요기요 리뷰와 배달평점 정보를 스크래핑
    """
    store_name2num = {"BHC-문래" : 60641,
        "호식이두마리치킨" : 218999,
        "구로동중앙점" : 432305,
        "KFC-당산역점" : 279243,
        "또래오래-영등포구청점" : 230241,
        "교촌치킨-당산점" : 253503,
        "굽네치킨&피자-신도림점" : 317759,
        "교촌치킨-영등포역점" : 479553,
        "소풍엄지척닭강정-구로점" : 286059,
        "후라이드참잘하는집-영등포점" : 252786
        }

    for name in ar:
        browser = webdriver.Chrome(os.path.join(os.getcwd(), 'hong/chromedriver.exe'))
        browser.get("https://www.yogiyo.co.kr/mobile/?gclid=CjwKCAiA_omPBhBBEiwAcg7smUH9rurkJNYSxu08Ohu_7JxNMKsg_LIMAcBbArCWRDcK2EBRab_LbRoCvYQQAvD_BwE#/{}/".format(store_name2num[name]))
        time.sleep(1)
        # 리뷰 보기
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/div[1]/ul/li[2]')))
        except:
            print('link not find')
            browser.quit()
        elem = browser.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]')
        elem.click()
        time.sleep(1)

        # list 뽑기
        i = 0
        while(True):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            i+=1
            if i == 1:
                time.sleep(1)
                try:
                    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="review"]/li[12]')))
                except:
                    print('xpath not find')
                    continue
                down = browser.find_element_by_xpath('//*[@id="review"]/li[12]')
                down.click()
                cr_num = 0
                soup = BeautifulSoup(browser.page_source, "lxml")
                comment_list = soup.findAll("li", attrs={"class":"list-group-item star-point ng-scope"})
            else:
                try:
                    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="review"]/li[12]')))
                except:
                    print('xpath not find')
                    continue
                try:
                    down.click()
                except:
                    break
                time.sleep(3)
                cr_num = len(comment_list)
                soup = BeautifulSoup(browser.page_source, "lxml")
                comment_list = soup.findAll("li", attrs={"class":"list-group-item star-point ng-scope"})
                print("cr : ", cr_num)
                print("current list num : ", len(comment_list))

        # 브라우저 종료    
        browser.quit()

        print("list num", len(comment_list))
        # browser.find_elements_by_class_name("team-link ")

        rank_list = [rank.findAll("span", attrs={"class":"category"})[-1].text for rank in comment_list]
        # rank = comment_list[0].findAll("span", attrs={"class":"points ng-binding"})[-1].text
        review_c_list = [rev.find("p", attrs={"class":"ng-binding"}).text for rev in comment_list]
        # review_c = comment_list[0].find("p", attrs={"class":"ng-binding"}).text

        df = pd.DataFrame({"comment":review_c_list, "rank":rank_list})
        print("*" * 100)
        print("data print")
        print(df.tail())

        com = pyautogui.confirm("csv 저장 하실?" , "확인")
        if com == "OK":
            print("csv 파일로 저장합니다...")
            df.to_csv(os.path.join(os.getcwd(), "data/{}_comment.csv".format(name)), index=False)

yogiyo_scrapping("굽네치킨&피자-신도림점")