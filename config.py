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
import pandas

df = pandas.read_csv('LoginInfo.csv')
for i in range(df.size):
    print(str(df.values[i][0]).split('\t'))
print(str(df.values[0][0]).split('\t'))