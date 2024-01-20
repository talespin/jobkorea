import os
import math
import pandas as pd


def main():
    split_cnt = int(input("몇개의 파일로 나눌까요?\r\r(숫자만입력해주세요)"))
    if not os.path.exists('../list/jobkorea.xlsx'):
        print(os.path/abspath('../list/jobkorea.xlsx') + ' 파일이 없습니다. jobkorea_list.py 를 실행해서 먼저 리스트파일을 생성하세요')
        return
    df = pd.read_excel('../list/jobkorea.xlsx')
    if len(df) < split_cnt:
        print('건수보다 나누려는 수가 큽니다.')
        return
    page_cnt = math.ceil(len(df) / split_cnt)
    for cnt in range(0, split_cnt):
        df[cnt *page_cnt:(cnt+1)*page_cnt].to_json(f'../list/jobkorea_{cnt+1}.json', orient='records', force_ascii=False)



if __main__=='__main__':
    main()

