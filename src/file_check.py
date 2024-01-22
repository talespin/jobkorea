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
#https://www.jobkorea.co.kr/NET/jkWebModule/jkConfirm.aspx?r=1&a=/NET&ret=%2frecruit%2fjoblist%3fmenucode%3dlocal%26localorder%3d1
#보안문자 입력 후 다시 이용 가능합니다.
