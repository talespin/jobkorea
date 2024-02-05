import os
import orjson as json
from multiprocessing import Pool


def main():
    display = os.environ['DISPLAY']
    items = None
    lst = []
    with open('../list/jobkorea_1.json', 'rt', encoding='utf-8') as fs:
        items = json.loads(fs.read())
    for i, item in enumerate(items):
        server = (i % 10) +1
        id = item['id']
        url = item['url']
        pgm = f'rsh crawler{server} \'export DISPLAY={os.environ["DISPLAY"]};cd /mnt/work/jobkorea/src;python 3.jobkorea_crawler_one.py -i {id} -u "{url}" -d "{display}"\'
        lst.append(pgm)
    pool = Pool(10)
    pool.map_async(os.popen, lst)
    pool.close()
    pool.join()
    pool = None


if __name__=='__main__':
    main()
