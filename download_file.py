import wget
import os

# lzh圧縮ファイルを公式サイトからダウンロード 
def download_file(obj, date):
    ymd = date.replace('-', '')
    S, s = ('K', 'k') if obj == 'results' else ('B', 'b')
    if os.path.exists(f'downloads/{obj}/{ymd}.txt'):
        return
    else:
        os.makedirs(f'downloads/{obj}', exist_ok=True)
        try:
            url_t = f'http://www1.mbrace.or.jp/od2/{S}/'
            url_b = f'{ymd[:-2]}/{s}{ymd[2:]}.lzh'
            wget.download(url_t + url_b, f'downloads/{obj}/{ymd}.lzh')

        except:
            print(f'There are no data for {date}')

# 使用例
obj = 'results'  # 結果のオブジェクトを指定
date = '2023-10-20'

download_file(obj, date)
