import subprocess
import time
from urllib.parse import urljoin

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://crowdworks.jp/public/jobs/group/development'
#
# webdriver からクラウドワークスへアクセス
#
driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)
#
# python かつ募集中を✓
#
box = driver.find_element_by_name('search[keywords]')
box.send_keys('python')
box.submit()
check_box = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div/div[2]/section[1]/div[2]/div[1]/div/div[2]/label[1]/input')
check_box.click()
time.sleep(4)
#
# 結果をパース
#
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
driver.quit()
#
# 必要項目をスクレイピング
#
item_title = []
payment = []
due_date = []
abs_url = []
for i in soup.find_all('div', {'class': 'job_data_row'}):
    item = i.find('h3', {'class': 'item_title'}).text.strip()
    pay = i.find('div', {'class': 'entry_data payment'}).text.strip()
    due = i.find('div', {'class': 'entry_data expires'}).text.strip()
    rel_url = i.find('a', {'data-item-title-link': True}).get('href')
    abst = urljoin(url, rel_url)
    item_title.append(item)
    payment.append(pay)
    due_date.append(due)
    abs_url.append(abst)
#
# CSV出力
#
df = pd.DataFrame({'タイトル': item_title, '金額': payment, '期限': due_date, 'URL': abs_url})
df.to_csv('output.csv')
#
# Numbers で開く
#
args = ['open', '-a', '/Applications/Numbers.app', 'output.csv']
try:
    res = subprocess.check_call(args)
    print(res)
except:
    print('Error')
