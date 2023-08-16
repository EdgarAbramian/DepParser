import time
from multiprocessing import Process
import pandas
import logging
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from selenium.webdriver.chrome.options import Options


session_timeing = {"start":0}

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.3.904 Yowser/2.5 Safari/537.36")
opts.set_capability('unhandledPromptBehavior', 'accept')

driver = webdriver.Chrome(options=opts)

BASE_URL = "https://online.hcsbk.kz"
LOGIN_URL = "/UserAccount/Login?ReturnUrl=%2f"
FIND_URL="/AuctionLotFindDeposit/Find"

logging.basicConfig(level=logging.INFO, filename="dep_log.log",filemode="a")


WIN_STRS = ["Соның ішінде, Сіздің артық төлеміңіз", "Ақшалай қаражаттарды аударуға арналған шот"]
def Refresher(akkName):
    if (time.time() - session_timeing['start']) // 60 >= 10:
        driver.refresh()
        logging.info(f'UserName: {akkName} time: {datetime.datetime.now()} PAGE IS REFRESHED')
        session_timeing['start'] = int(time.time())

def ByPassAlert(driver = driver):
    try:
        driver.switch_to.alert.accept()
    except NoAlertPresentException:
        pass

Accumulation = lambda concessions, overpayment: concessions - overpayment

Commission = lambda accum: accum * 0.5

Reward = lambda overpayment, commission: overpayment - commission

Coeff = lambda accum, reward: accum // reward

def login_func(driver=driver, username='', password=''):

    driver.get(BASE_URL + LOGIN_URL)

    session_timeing['start'] = int(time.time())

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

    driver.get(BASE_URL + FIND_URL)

    logging.info(f'\nNEW SESSION CREATED AT {datetime.datetime.now()}\n')

    time.sleep(5)

def GetVal(htmlCode):
    soup = BeautifulSoup(htmlCode, features="html.parser")

    sum_ust = int(str(soup.find('div',
                    class_ = "modal fade inheritModalPopup univer"
                             "sal-modal-form ui-draggable show").find('div','SumDiv').select("span")).split('\n')[4].replace(' ','').replace('\xa0',''))

    perepl = (int(soup.find('div',
                    class_ = "modal fade inheritModalPopup univer"
                             "sal-modal-form ui-draggable show").find('div','HOne').select("span")[0].text.split('<')[0].replace('\xa0','')))

    return {'sum_ust': sum_ust, 'perepl': perepl}

DIR_CONDITION = {'FOR':True,'BACK':False}
def find_dep(driver = driver, coef=0, akkName='', email='', MIN_DEP_ID=0):
    global soup
    DEP_IDS = {'cur':MIN_DEP_ID + 1,'min':MIN_DEP_ID, 'max':MIN_DEP_ID+300}


    while True:

            #   ЗАПРОС ПО ID  В КОНСОЛИ
            try:
                driver.execute_script(f"SendAll('{DEP_IDS['cur']},')")

            except:
                logging.warning(f'UserName: {akkName} time: {datetime.datetime.now()} ID:{DEP_IDS["cur"]} response: Script is not executed (ID is skipped)')

            soup = BeautifulSoup(driver.page_source, features="html.parser")

            time.sleep(2)

            ByPassAlert()

            #   ЕСЛИ ДОШЛИ ДО ВЕРХНЕГО ЗНАЧЕНИЯ ID
            if (DEP_IDS['cur'] == DEP_IDS['max']):
                # ИЗМЕНЯЕТСЯ НАПРАВЛЕНИЕ
                DIR_CONDITION['BACK'], DIR_CONDITION['FOR'] = DIR_CONDITION['FOR'], DIR_CONDITION['BACK']
                print(DEP_IDS['max'])

            #   ЕСЛИ ДОШЛИ ДО СТАРТОВОГО ЗНАЧЕНИЯ ID
            elif ((DEP_IDS['cur'] == DEP_IDS['min'])):
                # ИЗМЕНЯЕТСЯ НАПРАВЛЕНИЕ
                DIR_CONDITION['BACK'], DIR_CONDITION['FOR'] = DIR_CONDITION['FOR'], DIR_CONDITION['BACK']
                print("DEP_IDS['min'])")

            #   ОТКРЫАНИЕ ОКНА ДЕП КУПЛЕН ИЛИ ДОСТУПН
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'UniversalModalFormForm')))

            except TimeoutException:
                logging.warning(f'UserName: {akkName} time: {datetime.datetime.now()} ID:{DEP_IDS["cur"]} response: WINDOW IS NOT FIND ')


            #   РАБОТА С ОКНОМ ПРОДАННОГО ДЕПА
            if ("Сіз салымды төмендегі себептерге байланысты сатып ала алмайсыз:" in str(soup.find(id="UniversalModalFormForm").text)):
                    # ЗАКРЫВАЕНИЕ ОКНА ПРОДАННОГО ДЕПА
                    try:
                        driver.find_element(By.XPATH,'//*[@id="UniversalModalForm"]/div/div/div[1]/button/span').click()
                    except:
                        pass


            #   ОБНАРУЖЕНИЕ ДЕПА КОТОРЫЙ МОЖНО КУПИТЬ
            elif (WIN_STRS[0] in str(soup.find(id="UniversalModalFormForm").text) or WIN_STRS[1] in str(soup.find(id="UniversalModalFormForm").text)):
                vals = GetVal(driver.page_source)
                accum = Accumulation(vals["sum_ust"],vals["perepl"])
                comm = Commission(accum)
                rew = Reward(vals["perepl"], comm)
                cef = accum//rew

                #   ПРОВЕРКА КОЭФФИЦЕНТА
                if (abs(coef - cef) == cef):
                    driver.save_screenshot(f"{DEP_IDS}.png")

                    try:
                        driver.find_element(By.XPATH, '//*[@id="Agree"]').click()

                        Email = driver.find_element(By.XPATH, '//*[@id="Email"]')
                        Email.click()
                        Email.clear()
                        Email.send_keys(email)

                        driver.find_element(By.XPATH,'//*[@id="BodyModal"]/div/button').click()
                    except:
                        pass

                    #   ЗАСЫПАЕТ НА 5 МИН И ВОЗВРАЩАЕТСЯ К СТРАНИЦЕ ПОИСКА
                    time.sleep(300)
                    driver.get(BASE_URL + FIND_URL)

            #   ПОЛУЧАЕМ ЛОГГИ ОТ BROWSER
            LOGS = driver.get_log("browser")

            #   ПРОВЕРЯЮ ЛОГГИ
            if len(LOGS) != 0:
                        msg = (
                            f'UserName: {akkName} time: {datetime.datetime.now()} ID:{DEP_IDS["cur"]} response: {LOGS[len(LOGS) - 1]}')  # , status:{requests.get(url=str(LOGS[0]["message"]).split(" ")[0]).status_code}
                        logging.info(msg)
                        #ПРОВЕРКА НА ОШИБКУ 500 ПРИ ДВИЖЕНИИ ВПЕРЕД
                        for log in LOGS:
                            if "500 (Internal Server Error)" in str(log) and DIR_CONDITION["FOR"]:
                                DIR_CONDITION["FOR"], DIR_CONDITION["BACK"] = DIR_CONDITION["BACK"], DIR_CONDITION["FOR"]
                                DEP_IDS['max'] = DEP_IDS['cur']
                                break

            #   ПУСТЫЕ ЛОГГИ ОТ BROWSER
            else:
                    logging.info(f'UserName: {akkName} time: {datetime.datetime.now()} ID:{DEP_IDS["cur"]} NO RESPONSE')

            #   ОБНОВЛЯЕТ СТРАНИЦУ ПОИСКА КАЖДЫЕ 10 МИН
            Refresher(akkName)

            time.sleep(1)

            if (DIR_CONDITION['FOR']):
                DEP_IDS["cur"] += 1
            else:
                DEP_IDS["cur"] -= 1

def parser(username = '',password = '', coef=0, akkName='',email='',MIN_DEP_ID=0):
    try:
        print(username)
        login_func(username=username, password=password)
        time.sleep(5)
        find_dep(coef=coef, akkName=akkName, email=email,MIN_DEP_ID=MIN_DEP_ID)
    except:
        print("ERORR")
    finally:
        driver.close()
        driver.quit()

if __name__ == "__main__":
    cl_list = []
    df = pandas.read_csv('LoginInfo.csv')
    processes = []
    for i in range(df.size):
        acc_info = (str(df.values[i][0]).split('\t'))
        p = Process(target=parser, args=(acc_info[0],acc_info[1],int(acc_info[2]),acc_info[3],acc_info[4],int(acc_info[5])))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()




#Ақшалай қаражаттарды аударуға арналған шот
#Соның ішінде, Сіздің артық төлеміңіз
