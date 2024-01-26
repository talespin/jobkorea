#!/usr/bin/python
"""
:filename: 4.jobkorea_parser_one.py
:author: 최종환
:last update: 2024.01.11
 
:CHANGELOG:
    ============== ========== ====================================
    수정일            수정자        수정내용
    ============== ========== ====================================
    2024.01.11     최종환        최초생성
    ============== ========== ====================================
 
:desc:
    jobkorea crawl 파일 파싱 id 별 하나씩 파싱하여 id.json 으로 결과생성
"""
import os
import sys
import logging
import orjson as json
from glob import glob
from bs4 import BeautifulSoup as bs



def clear_dblspace(s:str)->str:
    while True:
        if len(s) == len(s.replace('  ','')): return s
        s = s.replace('  ','')


def main():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    ids = [os.path.basename(x) for x in glob('../crawl/*')]
    for i, recruit_id in enumerate(ids):
        print(f'{i+1} / {len(ids)}')
        try:
            if os.path.exists(f'../crawl/{recruit_id}/{recruit_id}.json'): continue
            with open(f'../crawl/{recruit_id}/{recruit_id}.html', 'rb') as fs:
                if fs.read().decode('utf-8').find('채용공고가 존재하지 않습니다') >= 0:
                    logging.info(' 채용공고가 존재하지 않습니다')
                    os.remove(f'../crawl/{recruit_id}/{recruit_id}.html')
                    os.removedirs(f'../crawl/{recruit_id}')
                    continue             
                doc = bs(fs.read(), 'html.parser')
            title = json.loads(doc.find_all('script')[-2].text.strip())['title']
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
            with open(f'../crawl/{recruit_id}/{recruit_id}.json', 'wt') as fs:
                _ = fs.write(json.dumps(dct).decode('utf-8'))
        except Exception as e:
            logging.error(f'parse error:{recruit_id}')
            logging.error(str(e))


if __name__=='__main__':
    main()

