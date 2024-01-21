#!/usr/bin/python
"""
:filename: jobkorea_crawler.py
:author: 최종환
:last update: 2024.01.11
 
:CHANGELOG:
    ============== ========== ====================================
    수정일            수정자        수정내용
    ============== ========== ====================================
    2024.01.11     최종환        최초생성
    ============== ========== ====================================
 
:desc:
    jobkorea site 의 지역별 체용정보 전체검색
 
"""
import os
import sys
import urllib3
import logging
import argparse
import pandas as pd
import requests as req
from random import random
from time import sleep
from bs4 import BeautifulSoup as bs


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def clear_dblspace(s:str)->str:
    while True:
        if len(s) == len(s.replace('  ','')): return s
        s = s.replace('  ','')


def jobkorea_crawler(list_file:str, overwrite:bool = False):
    if not os.path.exists(list_file):
        print('File not found:' + os.path.abspath(list_file))
        return
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.jobkorea.co.kr',
        'Referer': 'https://www.jobkorea.co.kr/recruit/joblist?menucode=local&localorder=1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    #세션 및 쿠키생성
    session = req.Session()
    base_url = 'https://www.jobkorea.co.kr'
    res = session.get(base_url, headers=headers, verify=False)
    cookies = dict(res.cookies)
    items = pd.read_json(list_file).to_dict('records')    
    #페이지 상세조회
    for item in items:
        recruit_id = item['id']
        os.makedirs(f'../crawl/{recruit_id}', exist_ok=True)	
        url = item['url']
        if os.path.exists(f'../crawl/{recruit_id}/{recruit_id}.html') and not overwrite:
            logging.info(f'    Skip file exists:{recruit_id}/{recruit_id}.html')
            continue
        sleep(10*random())
        logging.info(f'      crawling:{recruit_id}')
        res = req.get(url, headers=headers, cookies=cookies, verify=False)
        with open(f'../crawl/{recruit_id}/{recruit_id}.html', 'wb') as fs:
            fs.write(res.content)
        doc = bs(res.content, 'html.parser')
        ##article
        _article = doc.find('article', {'class':'artReadJobSum'})
        article = {}
        for dt, dd in zip(_article.find_all('dt'), _article.find_all('dd')):   
            article.update({dt.text.strip():''.join([clear_dblspace(k).strip() for k in dd.text.strip().split('\r\n')])})
        try:
            article.update({'지역':article.get('지역').replace('지도','').strip()})
        except:
            pass
        ##company
        _company = doc.find('div', {'class':'tbCol tbCoInfo'})
        company = {}
        for dt, dd in zip(_company.find_all('dt'), _company.find_all('dd')):
            company.update({dt.text.strip(): ''.join([clear_dblspace(x) for x in dd.text.strip().split('\r\n')])})
        ##recruit
        url = base_url + [x.get('src') for x in doc.find_all('iframe') if str(x.get('src')).startswith('/Recruit/GI_Read_Comt_Ifrm')][0]
        res = req.get(url, headers=headers, cookies=cookies, verify=False)
        _tables = bs(res.content, 'html.parser').find_all('table')
        for i, table in enumerate(_tables):
            with open(f'../crawl/{recruit_id}/{i}.html', 'wt', encoding='utf-8') as fs:
                fs.write(str(table))
			

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    parser = argparse.ArgumentParser(
                    prog='jobkorea crawler',
                    description='jobkorea 구인목록을 크롤합니다.')
    parser.add_argument('-l', '--list')
    parser.add_argument('-o', '--overwrite', default=False)
    args = parser.parse_args()
    jobkorea_crawler(args.list, args.overwrite)

