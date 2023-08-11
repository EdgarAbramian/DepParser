
import time
import requests
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import logging
import datetime
import pandas
import threading
from config import opts
ua = UserAgent()
# SendAll('119085,')
load_dotenv()

MIN_DEP_ID = 119185

driver = webdriver.Chrome(options=opts)

BASE_URL = "https://online.hcsbk.kz"
LOGIN_URL = "/UserAccount/Login?ReturnUrl=%2f"
FIND_URL="/AuctionLotFindDeposit/Find"

logging.basicConfig(level=logging.INFO, filename="dep_log.log",filemode="a")

Accumulation = lambda concessions, overpayment: concessions - overpayment

Commission = lambda accum: accum * 0.5

Reward = lambda overpayment, commission: overpayment - commission

Coeff = lambda accum, reward: accum // reward

def login_func(driver=driver, username='', password=''):

    driver.get(BASE_URL + LOGIN_URL)

    login_btn = driver.find_element(By.ID,"loginButton")

    UserNameInput = driver.find_element(By.XPATH,'//*[@id="UserName"]')
    PasswordInput = driver.find_element(By.XPATH,'//*[@id="Password"]')

    UserNameInput.click()
    UserNameInput.clear()
    UserNameInput.send_keys(username)

    PasswordInput.click()
    PasswordInput.clear()
    PasswordInput.send_keys(password)

    login_btn.click()

def find_dep(driver = driver, coef=0, akkName='',email=''):

    global CUR_DEP_ID
    CUR_DEP_ID =MIN_DEP_ID
    FOR_DEP = True
    BACK_DEP = False

    driver.get(BASE_URL + FIND_URL)
    time.sleep(5)

    while FOR_DEP:
        try:
            driver.execute_script(f"SendAll('{CUR_DEP_ID},')")
            soup = BeautifulSoup(driver.page_source, features="html.parser")

            time.sleep(3)
            try:

                driver.switch_to.alert.accept()
            except NoAlertPresentException:
                pass
            LOGS = driver.get_log("browser")
            if LOGS:
                msg = (
                    f'UserName: {akkName} time: {datetime.datetime.now()} ID:{CUR_DEP_ID} response: {LOGS[0]["message"]}, status:{requests.get(url=str(LOGS[0]["message"]).split(" ")[0]).status_code} ')
                logging.info(msg)
            else:
                logging.info(f'UserName: {akkName} time: {datetime.datetime.now()} ID:{CUR_DEP_ID} NO RESPONSE')


            try:
                 pop_win = (WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'UniversalModalForm'))))
                 with open(f"DepStatus.txt", "a", encoding="utf-8") as winfile:
                      winfile.write('\n')
                      winfile.write(f'{CUR_DEP_ID}: {soup.find(id="UniversalModalForm")}')

            except TimeoutException:
                    pass

            if int(requests.get(url=str(LOGS[0]["message"]).split(" ")[0]).status_code) == 500:
                    FOR_DEP, BACK_DEP = BACK_DEP, FOR_DEP

            time.sleep(10)

        except:
            driver.refresh()
            time.sleep(5)
            driver.execute_script(f"SendAll('{CUR_DEP_ID},')")
            soup = BeautifulSoup(driver.page_source, features="html.parser")

            time.sleep(3)
            try:
                # switch to alert and click ok button
                driver.switch_to.alert.accept()
            except NoAlertPresentException:
                pass
            LOGS = driver.get_log("browser")
            if LOGS:
                msg = (
                    f'UserName: {akkName} time: {datetime.datetime.now()} ID:{CUR_DEP_ID} response: {LOGS[0]["message"]}, status:{requests.get(url=str(LOGS[0]["message"]).split(" ")[0]).status_code} ')
                logging.info(msg)
            else:
                logging.info(f'UserName: {akkName} time: {datetime.datetime.now()} ID:{CUR_DEP_ID} NO RESPONSE')

            try:
                pop_win = (WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'UniversalModalForm'))))

                with open(f"DepStatus.txt", "a", encoding="utf-8") as winfile:
                    winfile.write('\n')
                    winfile.write(f'{CUR_DEP_ID}: {soup.find(id="UniversalModalForm")}')

            except TimeoutException:
                    print("Loading took too much time!")

            if int(requests.get(url=str(LOGS[0]["message"]).split(" ")[0]).status_code) == 500:
                    FOR_DEP, BACK_DEP = BACK_DEP, FOR_DEP

        time.sleep(10)
        CUR_DEP_ID += 1

    '''ИДЕТ НАЗАД ПО ID'''
    while BACK_DEP:
        try:
            driver.execute_script(f"SendAll('{CUR_DEP_ID},')")
            LOGS = driver.get_log("browser")
            if LOGS:
                msg = (
                    f'UserName: {akkName} time: {datetime.datetime.now()} ID:{CUR_DEP_ID} response: {LOGS[0]["message"]}, status:{requests.get(url=str(LOGS[0]["message"]).split(" ")[0]).status_code} ')
                logging.info(msg)
            else:
                logging.info(f'UserName: {akkName} time: {datetime.datetime.now()} ID:{CUR_DEP_ID} NO RESPONSE')

            try:
                pop_win = (WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'UniversalModalForm'))))

                FOR_DEP, BACK_DEP = BACK_DEP, FOR_DEP

                with open(f"DepStatus.txt", "a", encoding="utf-8") as winfile:
                    winfile.write('\n')
                    winfile.write(f'{CUR_DEP_ID}: {soup.find(id="UniversalModalForm")}')

            except TimeoutException:
                print("Loading took too much time!")

            time.sleep(10)

        except:
            driver.refresh()
            time.sleep(10)
            driver.execute_script(f"SendAll('{CUR_DEP_ID},')")

            LOGS = driver.get_log("browser")
            if LOGS:
                msg = (
                    f'UserName: {akkName} time: {datetime.datetime.now()} ID:{CUR_DEP_ID} response: {LOGS[0]["message"]}, status:{requests.get(url=str(LOGS[0]["message"]).split(" ")[0]).status_code} ')
                logging.info(msg)
            else:
                logging.info(f'UserName: {akkName} time: {datetime.datetime.now()} ID:{CUR_DEP_ID} NO RESPONSE')

            try:
                pop_win = (
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'UniversalModalForm'))))

                FOR_DEP, BACK_DEP = BACK_DEP, FOR_DEP

                with open(f"DepStatus.txt", "a", encoding="utf-8") as winfile:
                    winfile.write('\n')
                    winfile.write(f'{CUR_DEP_ID}: {soup.find(id="UniversalModalForm")}')

            except TimeoutException:
                pass

            time.sleep(10)
        CUR_DEP_ID -= - 1

def parser(username = '',password = '', coef=0, akkName='',email=''):
    try:
        print(username)
        login_func(username=username, password=password)
        time.sleep(5)
        find_dep(coef=coef, akkName=akkName, email=email)
    except:
        print("ERORR")
    finally:
        driver.close()
        driver.quit()

if __name__ == "__main__":
    cl_list = []
    df = pandas.read_csv('LoginInfo.csv')
    for i in range(df.size):
        acc_info = (str(df.values[i][0]).split('\t'))
        # parser(acc_info[0],acc_info[1],int(acc_info[2]),acc_info[3],acc_info[4])
        client =threading.Thread(target=parser, args=(acc_info[0],acc_info[1],int(acc_info[2]),acc_info[3],acc_info[4]))
        cl_list.append(client)

    for cl in cl_list:
        cl.daemon = True
        cl.start()

    for cl in cl_list:
        cl.join()


