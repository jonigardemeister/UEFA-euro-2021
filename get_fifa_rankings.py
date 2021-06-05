#!/usr/bin/python

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd

row_list = list()
columns = ['date','rank','team','points']

driver = webdriver.Chrome("/Library/Frameworks/Python.framework/Versions/3.9/bin/chromedriver")

ids = ['12252', '12280', '12315', '12350', '12385', '12406', '12455', '12511', '12582', '12623', 
'12679', '12714', '12749', '12770', '12833', '12882', '12883', '12884', '13043', '13078', '13113', '13127', 
'13197', '13245', '13295']

for id in ids:
    url = "https://www.fifa.com/fifa-world-ranking/ranking-table/men/rank/id"+id+"/#UEFA"
    print(url)
    driver.get(url)

    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    index = 0

    date = soup.find('div', {"class": "fi-selected-item"}).text

    table = soup.find('table', {"id": "rank-table"})
    rows = table.find('tbody').find_all('tr')

    for tr in rows:
        rank = tr.find('td', {"class": "fi-table__rank"}).text
        print("rank = ", rank)
        team = tr.find('td', {"class": "fi-table__teamname"}).find('span', {"class": "fi-t__nText"}).text
        print("team = ", team)
        points = tr.find('td', {"class": "fi-table__points"}).text
        print("points = ", points)
        row = [date, rank, team, points]
        if(len(row) == 4):
            row_list.append(row)

df = pd.DataFrame(row_list, columns=columns)
print(df.shape)
df.to_csv('fifa_rankings.csv', index=False, encoding='utf-8-sig')
index += 1

df = pd.DataFrame(row_list,columns=columns)
df.dropna(subset=columns, inplace=True)
df.to_csv('fifa_rankings.csv', index=False, encoding='utf-8-sig')

driver.quit()
