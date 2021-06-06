#!/usr/bin/python

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd

df_teams = pd.read_csv('teams.csv', encoding='utf-8')
row_list = list()
columns = ['Date','Match','Result','Score','Competition']

driver = webdriver.Chrome("/Library/Frameworks/Python.framework/Versions/3.9/bin/chromedriver")

for team in df_teams['Country']:
    print(team)
    for year in ['2019', '2020', '2021']:
        url = "https://www.11v11.com/teams/"+team+"/tab/matches/season/"+year
        print(url)
        driver.get(url)

        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        index = 0

        table = soup.find('table')
        rows = table.find_all('tr')

        for tr in rows:
            td = tr.find_all('td')
            row = [i.text for i in td]
            if(len(row) == 5):
                row_list.append(row)

    df = pd.DataFrame(row_list, columns=columns)
    print(df.shape)
    df.to_csv('original_game_results.csv', index=False, encoding='utf-8-sig')
    index += 1

df = pd.DataFrame(row_list,columns=columns)
df.dropna(subset=columns, inplace=True)
df.to_csv('original_game_results.csv', index=False, encoding='utf-8-sig')
