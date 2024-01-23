#!/usr/bin/python
"""
:filename: 3.jobkorea_crawler.py
:author: 최종환
:last update: 2024.01.11
 
:CHANGELOG:
    ============== ========== ====================================
    수정일            수정자        수정내용
    ============== ========== ====================================
    2024.01.11     최종환        최초생성
    ============== ========== ====================================
 
:desc:
    jobkorea 옵션으로 지정한 json 파일을 읽어서 해당파일의 목록일 이용하여 컨텐츠를 크롤한다.
 
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
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def clear_dblspace(s:str)->str:
    while True:
        if len(s) == len(s.replace('  ','')): return s
        s = s.replace('  ','')


def jobkorea_crawler(list_file:str, overwrite:bool = False):
    if not os.path.exists(list_file):
        print('File not found:' + os.path.abspath(list_file))
        return
    #chapcha 를 대비하여 chrome 브라우저를 띄울 준비        
    chrome_svc = Service(os.path.abspath('chromedriver'))        
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
        sleep(30*random())
        logging.info(f'      crawling:{recruit_id}')
        #chapcha 가 표시되는지 확인하여 chapcha 처리후 진행되도록
        while True:
            res = req.get(url, headers=headers, cookies=cookies, verify=False)
            if res.text.find('보안문자') > 0:
                logging.warning("IP 차단 웹브라우저를 열어봅시다.")
                chrome = webdriver.Chrome(service=chrome_svc)
                chrome.get(url)
                input_capcha = input("보안문자를 입력했나요?\r\nY 를 입력하세요")
                chrome.close()
            else:
                with open(f'../crawl/{recruit_id}/{recruit_id}.html', 'wt', encoding='utf-8') as fs:
                    fs.write(res.content)
                break               
        doc = bs(res.content, 'html.parser')
        ##article
        _article = doc.find('article', {'class':'artReadJobSum'})
        article = {}
        dts, dds = None, None
        dts, dds = _article.find_all('dt'), _article.find_all('dd')
        for dt, dd in zip(dts, dds):
            try:
                article.update({dt.text.strip():''.join([clear_dblspace(k).strip() for k in dd.text.strip().split('\r\n')])})
            except:
                logging.warning("IP 차단됬으니 60분 있다가 시작합니다.")
                sleep(60*60)
                res = req.get(url, headers=headers, cookies=cookies, verify=False)
                with open(f'../crawl/{recruit_id}/{recruit_id}.html', 'wt', encoding='utf-8') as fs:
                    fs.write(res.content)
                doc = bs(res.content, 'html.parser')
                ##article
                _article = doc.find('article', {'class':'artReadJobSum'})
                article = {}
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
    chrome_svc.stop()                


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    parser = argparse.ArgumentParser(
                    prog='jobkorea crawler',
                    description='jobkorea 구인목록을 크롤합니다.')
    parser.add_argument('-l', '--list')
    parser.add_argument('-o', '--overwrite', default=False)
    args = parser.parse_args()
    jobkorea_crawler(args.list, args.overwrite)

