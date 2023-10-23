import wget
import os
import datetime

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


obj_B = 'racelists'
obj_K = 'results'
counter = 1
start_date = datetime.datetime(2014, 1, 1)
end_date = datetime.datetime(2023, 9, 30)

while start_date <= end_date:
    str_date = str(start_date).split(' ')[0].replace('-', '')
    print(str_date)
    download_file(obj_B, str_date)
    download_file(obj_K, str_date)

    start_date += datetime.timedelta(days=1)
    counter += 1

print('finished!')
