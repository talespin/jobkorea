#!/usr/bin/python
"""
:filename: jobkorea_parser.py
:author: 최종환
:last update: 2024.01.11
 
:CHANGELOG:
    ============== ========== ====================================
    수정일            수정자        수정내용
    ============== ========== ====================================
    2024.01.11     최종환        최초생성
    ============== ========== ====================================
 
:desc:
    jobkorea crawl 파일 파싱
 
"""
import os
import orjson
import logging
import pandas as pd
from glob import glob
from bs4 import BeautifulSoup as bs


def clear_dblspace(s:str)->str:
    while True:
        if len(s) == len(s.replace('  ','')): return s
        s = s.replace('  ','')


def jobkorea_parser():
    ids = [os.path.basename(x) for x in glob('crawl/*')]
    result = []
    for recruit_id in ids:
        try:
            with open(f'crawl/{recruit_id}/{recruit_id}.html', 'rb') as fs:
                doc = bs(fs.read(), 'html.parser')
            title = orjson.loads(doc.find_all('script')[-2].text.strip())['title']
            _article = doc.find('article', {'class':'artReadJobSum'})
            company_name = _article.find('span').text.strip()
            article = {}
            for dt, dd in zip(_article.find_all('dt'), _article.find_all('dd')):   
                article.update({'article:'+dt.text.strip():''.join([clear_dblspace(k).strip() for k in dd.text.strip().split('\r\n')])})
            try:
                article.update({'article:'+'지역':article.get('지역').replace('지도','').strip()})
            except:
                pass	
            ##company
            _company = doc.find('div', {'class':'tbCol tbCoInfo'})
            company = {}
            for dt, dd in zip(_company.find_all('dt'), _company.find_all('dd')):
                company.update({'company:'+dt.text.strip(): ''.join([clear_dblspace(x) for x in dd.text.strip().split('\r\n')])})
            ##recruit
            tables = '\r\n'.join(sorted([os.path.relpath(x) for x in glob(f'crawl/{recruit_id}/*.html') if os.path.basename(x) != f'{recruit_id}.html']))
            dct = dict(id=recruit_id, company_name=company_name, title=title)
            dct.update(article)
            dct.update(company)
            dct.update(dict(표=tables))
            result.append(dct)
        except:
            logging.error(f'parse error:{recruit_id}')
            raise
    df = pd.DataFrame(result)
    cols = [x for x in df.columns if x not in ['id','company_name','title','표']]
    df.to_excel(f'result/result.xlsx', index=False, columns=['id','company_name','title']+cols+['표'])


if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG)
    jobkorea_parser()

