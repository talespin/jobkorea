#!/usr/bin/python
"""
:filename: 4.jobkorea_parser_one.py
:author: 최종환
:last update: 2024.06.04

:CHANGELOG:
    ============== ========== ====================================
    수정일            수정자        수정내용
    ============== ========== ====================================
    2024.01.11     최종환        최초생성
    2024.06.04     최종환        파싱항목변경
    ============== ========== ====================================

:desc:
    jobkorea crawl 파일 파싱 id 별 하나씩 파싱하여 id.json 으로 결과생성
"""
#업체명, 상세모집분야, 근무형태, 임금형태, 최소학력, 급여, 경력, 근무지역, 연관직무
#우대사항, 요구자격증, 핵심역량, 채용직급, 채용인원, 채용기업의산업

import os
import json
import pandas as pd
from glob import glob
from lxml import etree
from bs4 import BeautifulSoup as bs
import multiprocessing as mp



def get_채용명(doc):
    return ' '.join(doc.find('title').text.strip().split('|')[:-1]).strip()


def get_업체명(dom):
    return dom.xpath('//*[@id="container"]/section/div[1]/article/div[1]/h3/div/span')[0].text.strip()	


def get_상세모집분야(doc):
    return [x for x in str(doc.find_all('script')).split('\n') if x.find("window.dsHelper.registVal('_n_var44'")>0][0][40:-4]


def get_근무형태(doc):
    try:
        return doc.select("#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(2) > dl > dd:nth-child(2) > ul > li")[0].text.strip()
    except:
        return ''


def get_임금형태(doc):
    return doc.select("#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(2) > dl > dd:nth-child(4)")[0].text.strip()	

	
def get_최소학력(doc):
    try:
        return doc.select("#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(1) > dl > dd:nth-child(4) > strong")[0].text.strip()
    except:
        return ''


def get_급여(doc):
    return doc.select("#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(2) > dl > dd:nth-child(4)")[0].text.strip()	


def get_경력(doc):
    return doc.select("#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(1) > dl > dd:nth-child(2)")[0].text.strip()


def get_근무지역(doc):
    try:
        return doc.select("#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(2) > dl > dd:nth-child(6) > a")[0].text.strip()
    except:
        return doc.select("#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(2) > dl > dd:nth-child(4)")[0].text.strip()


def get_연관직무(doc):
    try:
        return doc.select("#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div.tbCol.tbCoInfo > dl > dd:nth-child(2) > text")[0].text.strip()
    except:
        return ''


def get_우대사항(doc):
    try:
        return doc.select("#popupPref > div > div > dl > dd:nth-child(2)")[0].text.strip()
    except:
        return ''


def get_요구자격증(doc):
    try:
        return doc.select("#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(1) > dl > dd:nth-child(6)")[0].text.strip()
    except:
        try:	
            return doc.select("#popupPref > div > div > dl > dd:nth-child(4)")[0].text.strip()
        except:
            return ''


def get_핵심역량(doc):
    pass


def get_채용직급(doc):
    try:
        return doc.select("#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(2) > dl > dd:nth-child(10)")[0].text.strip()
    except:
        return ''


def get_채용인원(doc):
    try:
        return doc.select("#detailArea > section.secReadStatistic > article > div.metricsContainer > div.metrics.metricsRate > div.value")[0].text.strip()
    except:
        return ''


def get_채용기업의산업(doc):
    try:
        return doc.select("#tab03 > article.artReadCoInfo.divReadBx > div > div.tbCol.coInfo > dl > dd:nth-child(2) > text")[0].text.strip()
    except:
        try:
            return doc.select("#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div.tbCol.tbCoInfo > dl > dd:nth-child(2) > text")[0].text.strip()
        except:
            return ''


def main():
    crawl_list = [os.path.basename(x) for x in glob('../crawl/*')]
    os.makedirs('../parsed', exist_ok=True)
    pool = mp.Pool(5)#CPU 갯수-1 개 정도로 돌리면됩니다.
    pool.map(sub, crawl_list)
    pool.close()
    pool.close()


def sub(id):    
    json_file = f'../parsed/{id}.json'
    if os.path.exists(json_file): return
    with open(f'../crawl/{id}/{id}.html', 'rt', encoding='utf-8') as fs:
        doc = bs(fs.read(), 'html.parser')
        dom = etree.HTML(str(doc))
    ID = id
    #print(ID, end=' ')
    채용명 = get_채용명(doc)
    업체명 = get_업체명(dom)
    상세모집분야 = get_상세모집분야(doc)
    근무형태 = get_근무형태(doc)
    임금형태 = get_임금형태(doc)
    최소학력 = get_최소학력(doc)
    급여 = get_급여(doc)
    경력 = get_경력(doc)
    근무지역 = get_근무지역(doc)
    연관직무 = get_연관직무(doc)
    우대사항 = get_우대사항(doc)
    요구자격증 = get_요구자격증(doc)
    핵심역량 = get_핵심역량(doc)
    채용직급 = get_채용직급(doc)
    채용인원 = get_채용인원(doc)
    채용기업의산업 = get_채용기업의산업(doc)
    data = dict(ID=ID, 채용명=채용명, 업체명=업체명, 상세모집분야=상세모집분야, 근무형태=근무형태, 임금형태=임금형태, 최소학력=최소학력, 급여=급여, 경력=경력, 근무지역=근무지역, 연관직무=연관직무, 우대사항=우대사항, 요구자격증=요구자격증, 핵심역량=핵심역량, 채용직급=채용직급, 채용인원=채용인원, 채용기업의산업=채용기업의산업)
    with open(json_file, 'wt', encoding='utf-8') as fs:
        _ = fs.write(json.dumps(data, ensure_ascii=False))	


if __name__=='__main__':
    main()



