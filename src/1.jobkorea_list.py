#!/usr/bin/python
"""
:filename: 1.jobkorea_list.py
:author: 최종환
:last update: 2024.01.20
 
:CHANGELOG:
    ============== ========== ====================================
    수정일            수정자        수정내용
    ============== ========== ====================================
    2024.01.20     최종환        최초생성
    ============== ========== ====================================
 
:desc:
    jobkorea site 의 지역별 체용정보 전체검색 목록
 
"""
import os
import re
import sys
import math
import urllib3
import logging
import argparse
import pandas as pd
import requests as req
from glob import glob
from time import sleep
from bs4 import BeautifulSoup as bs



def jobkorea_list(is_yes):
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.root.name='jobkorea_list'
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    ip = None
    while True:
        if is_yes: break     
        ip = input('>>>크롤작업을 새로 시작하려면 Y  이어서 하려면 N 를 입력하세요\n')
        if ip in ['Y','N']: break
    if ip == 'Y' or is_yes: [os.remove(x) for x in glob('../list/*')]
    logging.info('start crawl list jobkorea')
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
    #
    # #지역별 건수 구하기
    # url = f'{base_url}/recruit/joblist?menucode=local&localorder=1'
    # res = req.get(url, headers=headers, verify=False, cookies=cookies)
    # _areas = [x for x in doc.find_all('label', {'class':'lb_tag'}) if x.get('for').startswith("local_step1_")]
    # areas = []
    # doc.find('ul', {'data-category':"local"}).find_all()
    #for area in _areas:
    #    try:
    #        area_code = area.get('for')[-4:]
    #        [area_name, area_count] = area.find_all('span')[1].text.split('(')
    #        job_count = int(area_count[:-1].replace(',',''))
    #        areas.append(dict(area_code=area_code, area_name=area_name, job_count=job_count))
    #    except:
    #        logging.debug('parse error: ' + area.text)
    #지역별 목록조회
    total_page = 50
    _pagesize = 5000
    page = 1
    items = []
    while True:
        logging.info(f"    page={page} / {total_page}")
        data = {
            'page': f'{page}',
            'condition[menucode]': 'Q000',
            'direct': '0',
            'order': '20',
            'pagesize': f'{_pagesize}',
            'tabindex': '0',
            'onePick': '0',
            'confirm': '0',
            'profile': '0',
        }
        logging.debug(str(data))
        file_name = f'../list/{page}.page'
        if os.path.exists(file_name):
            with open(file_name,'rt', encoding='utf-8') as fs:
                doc = bs(fs.read(), 'html.parser')
        else:
            sleep(5)
            res = session.post(f'{base_url}/Recruit/Home/_GI_List/', cookies=cookies, headers=headers, data=data, verify=False)
            with open(file_name,'wt') as fs:
                fs.write(res.content.decode('utf-8'))
            doc = bs(res.content, 'html.parser')
        total_page = math.ceil(int(re.sub('\D','', doc.find('span', {'data-text':"전체"}).text)) / _pagesize)
        page = page+1
        if page > total_page: break
        _items = doc.find_all('td', {'class':'tplTit'})
        for item in _items:
            url = base_url + item.find('a').get('href')
            try:
                data_brazeinfo = item.find('button').get('data-brazeinfo')
            except:
                pass
            try:
                list_info = [x.text.strip() for x in item.find_all('span', {'class':'cell'})]
            except:
                pass
            items.append(dict(id=data_brazeinfo.split('|')[1], url=url, data_brazeinfo=data_brazeinfo, list_info=list_info))
    logging.info('crawl list jobkorea complete')
    #리스트 크롤완료
    logging.info('make list file processing...')
    os.makedirs('../list', exist_ok=True)
    #pd.DataFrame(items).to_excel(f"../list/jobkorea.xlsx", index=False)
    pd.DataFrame(items).to_csv(f"../list/jobkorea.csv", index=False)
    logging.info('complete!!!')



if __name__=='__main__':
    parser = argparse.ArgumentParser(prog='jobkorea list crawle', description='jobkorea 리스트를 크롤합니다') 
    parser.add_argument('-y')
    args = parser.parse_args()
    jobkorea_list(args.y)

