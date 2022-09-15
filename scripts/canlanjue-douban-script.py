"""
loading packages
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import math
import time 
import random
import pyuser_agent

def get_item_num():
    '''get total number of comments
    '''
    url = 'https://movie.douban.com/subject/34779776/comments?start=0&limit=100&status=P&sort=new_score'
    ua = pyuser_agent.UA()
    headers = {
          "User-Agent" : ua.random
    }
    response = requests.get(url=url, headers=headers)
    html = response.text
    # parse html
    soup = BeautifulSoup(html, 'html.parser')
    # total number of comments
    item_num = soup.find(class_='is-active').find('span').text
    item_num = int(re.findall(r'\d+', item_num)[0])
    return item_num

def get_items(page, page_limit):
    '''get comment items in one page
    '''
    url = f'https://movie.douban.com/subject/34779776/comments?start={page}&limit={page_limit}&status=P&sort=new_score'
    ua = pyuser_agent.UA()
    headers = {
          "User-Agent" : ua.random
    }
    response = requests.get(url=url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', attrs={'class': 'comment-item'})
    return items

def get_comments(data_dic_list, items):
    '''get all comments from one page
    '''
    for i in items:
        account_title = i.find(class_='avatar').find('a').get('title')
        account_link = i.find(class_='avatar').find('a').get('href')
        vote_num = i.find(class_='votes vote-count').text
        vote_num = int(vote_num)
        try:
            star = i.find(class_='rating').get('title') 
        except:
            star = None
        comment_time = i.find(class_='comment-time').get('title')
        comment_location = i.find(class_='comment-location').text
        comment = i.find(class_='comment-content').text.strip()
        dic = {
            'username': account_title,
            'profile_link': account_link,
            'vote_num': vote_num,
            'star': star,
            'comment_time': comment_time,
            'comment_location': comment_location,
            'comment': comment
        }
        data_dic_list.append(dic)

if __name__ == '__main__':
    page_limit = 100
    item_num = get_item_num()
    # total pages
    total_pages = math.ceil(item_num / page_limit)
    data_dic_list = []
    for page in range(0, total_pages):
        items = get_items(page, page_limit)
        get_comments(data_dic_list, items)
        time.sleep(0.5+random.uniform(0, 0.5))
        print(f'{page} is done')
    df = pd.DataFrame(data_dic_list)
    df.to_csv('../data/canglangjue_data.csv', index=False)
