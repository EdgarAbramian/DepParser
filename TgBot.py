import time
from math import ceil

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.3.904 Yowser/2.5 Safari/537.36'
# }
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.3.904 Yowser/2.5 Safari/537.36")
opts.set_capability('unhandledPromptBehavior', 'accept')

# resp_id = requests.get(url=f'https://online.hcsbk.kz/AuctionLotFindDeposit/BuyerCondition?selectAuctionDeposits={118594+i},&PublicKey=')
# print(resp_id.json())
# r =requests.post(url=f'https://online.hcsbk.kz/AuctionLotFindDeposit/BuyerCondition?selectAuctionDeposits={118503+i},&PublicKey=',data=data)


header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.google.com/'
}

#r = requests.get(url=f'https://online.hcsbk.kz/AuctionLotFindDeposit/BuyerCondition?selectAuctionDeposits={118594}').text
#"data": '{"H":"deposithub","M":"SendAll","A":["118493,"],"I":0}'
# data = {"H":"deposithub","M":"SendAll","A":["118493,"],"I":0}
import datetime

#
#
#
from bs4 import BeautifulSoup

# site_code = {'code':''}
#
# with open('D:\docs\Otbasy bank3.html','r', encoding='utf-8')as file:
#     site_code['code'] = str(file.read())


# def GetVal(htmlCode):
#     soup = BeautifulSoup(htmlCode, features="html.parser")
#
#     sum_ust = int(str(soup.find('div',
#                     class_ = "modal fade inheritModalPopup univer"
#                              "sal-modal-form ui-draggable show").find('div','SumDiv').select("span")).split('\n')[4].replace(' ','').replace('\xa0',''))
#
#     perepl = (int(soup.find('div',
#                     class_ = "modal fade inheritModalPopup univer"
#                              "sal-modal-form ui-draggable show").find('div','HOne').select("span")[0].text.split('<')[0].replace('\xa0','')))
#
#     return {'sum_ust': sum_ust, 'perepl': perepl}
#
#
# print(GetVal(site_code['code'])['sum_ust'])
# print(GetVal(site_code['code'])['perepl'])


# for i in range(df.size):
    #     acc_info = (str(df.values[i][0]).split('\t'))
    #     client = threading.Thread(target=parser, args=(acc_info[0],acc_info[1],int(acc_info[2]),acc_info[3],acc_info[4],int(acc_info[5])))
    #     cl_list.append(client)
    #
    # for cl in cl_list:
    #     cl.daemon = True
    #     cl.start()
    #
    # for cl in cl_list:
    #     cl.join()
# with open(f"{DEP_IDS['cur']}.txt", "w", encoding="utf-8") as winfile:
#     winfile.write(f'ID: {DEP_IDS["cur"]}\n')
#     winfile.write(f'Накопление: {accum}\n')
#     winfile.write(f'Комиссия: {comm}\n')
#     winfile.write(f'Вознаграждение: {rew}\n')
#     winfile.write(f'Кэф: {cef}\n')


# Accumulation = lambda ustup, perepl: ustup - perepl
#
# Commission = lambda accum: round(accum * 0.005)
#
# Reward = lambda perepl, commission: perepl - commission
#
# Coeff = lambda accum, reward: ceil(accum / reward)
#
# accum = Accumulation(1754521,65034)
# comm = Commission(accum)
# rew = Reward(65034, comm)
# cef = Coeff(accum,rew)
#
# print(f'accum: {accum}')
# print(f'comm: {comm}')
# print(f'rew: {rew}')
# print(f'cef: {cef}')





import telebot

PATH = ''

with open('path.txt','r') as file:
    PATH = str(file.read())

BOT_TOKEN = ''

with open('token.txt','r') as file:
    BOT_TOKEN = str(file.read())


bot = telebot.TeleBot(BOT_TOKEN)
TEXT = ''
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "BOT IS STARTED")
    while True:

        with open(PATH,'r',encoding="utf-8") as file:
            TEXT = file.read()

        if TEXT:
            bot.send_message(message.chat.id, f"{TEXT}")

            with open(PATH,'w',encoding="utf-8") as file:
                file.write(f"")

bot.infinity_polling()


















