import os
from glob import glob
from bs4 import BeautifulSoup as bs

ids = [os.path.basename(x) for x in glob('../crawl/*')]
for id in ids:
  try:
      with open(f'../crawl/{id}/{id}.html','rt') as fs:
        if fs.read().find('차단되었습니다') > 0:
          print(id)
  except:
    pass

