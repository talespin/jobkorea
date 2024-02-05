import os
import orjson as json
from multiprocessing import Pool
from time import sleep


def main():
    display = os.environ['DISPLAY']
    items = None
    lst = []
    with open('../list/jobkorea_1.json', 'rt', encoding='utf-8') as fs:
        items = json.loads(fs.read())
    for i, item in enumerate(items):
        id = item['id']
        if os.path.exists(f'../crawl/{id}/{id}.html'): continue
        server = (i % 10) +1
        url = item['url']
        pgm = f'rsh crawler{server} \'export DISPLAY={os.environ["DISPLAY"]};cd /mnt/work/jobkorea/src;/usr/share/python-3.11/bin/python 3.jobkorea_crawler_one.py -i {id} -u "{url}" -d "{display}"\''
        print(pgm)
        lst.append(pgm)
    pool = Pool(10)
    pool.map_async(subprocess, lst)
    pool.close()
    pool.join()
    pool = None


def subprocess(pgm):
    p = os.popen(pgm)
    #sleep(40)
    print(p.read())



if __name__=='__main__':
    main()
