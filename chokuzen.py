import re
import pandas as pd
import glob
import os
import mojimoji
import lhafile
from download_file import download_file

obj_B = 'results'
obj_K = 'racelists'

columns = [
    'Date', 'Round', '会場', '艇番', '選手登番', '選手名', '年齢', '支部', '体重', '級別', 
    '全国勝率', '全国２連率', '当地勝率', '当地２連率', 'モーター２連率', 'ボート２連率', '展示タイム', 'スタートタイム',
]

place_mapper = {
    1: '桐生', 2: '戸田', 3: '江戸川', 4: '平和島', 5: '多摩川',
    6: '浜名湖', 7: '蒲郡', 8: '常滑', 9: '津', 10: '三国',
    11: '琵琶湖', 12: '住之江', 13: '尼崎', 14: '鳴門', 15: '丸亀',
    16: '児島', 17: '宮島', 18: '徳山', 19: '下関', 20: '若松',
    21: '芦屋', 22: '福岡', 23: '唐津', 24: '大村'
}

date = str(input('解析したい番組表の日付(例：20230101)を入力してください... '))

# 必要なフォルダの作成、不要なファイルの削除
os.makedirs('./input/chokuzen', exist_ok=True)
filelist = glob.glob('./input/chokuzen/*')
for f in filelist:
    os.remove(f)

# 番組表、競争結果のファイルをダウンロード
download_B = download_file(obj_B, date)
download_K = download_file(obj_K, date)

# ダウンロードしたファイル(.lzh)を解凍
lha = lhafile.Lhafile(f'./downloads/racelists/{date}.lzh')
for info in lha.infolist():
    with open(f'./downloads/racelists/{info.filename}', 'wb') as f:
        f.write(lha.read(info.filename))

filepath = f'./downloads/racelists/B{date[2:]}.TXT'

all_place_data = pd.DataFrame()
raceNo_b = 1
data_list = []
with open(filepath, 'r', encoding='shift_jis') as f:
    while True:
        line = f.readline().replace('\u3000', '').replace('100.00', ' 99.99').replace('10.00', ' 9.99')
        data = mojimoji.zen_to_han(line)
        data_list.append(data)
        if 'FINALB' in data:
            break

pattern = '^([1-6])\s(\d{4})([^0-9]+)(\d{2})([^0-9]+)(\d{2})([AB]\d{1})\s(\d{1}.\d{2})\s*(\d+.\d{2})\s(\d{1}.\d{2})\s*(\d+.\d{2})\s+\d+\s+(\d+.\d{2})\s*\d+\s+(\d+.\d{2})'
pattern_re = re.compile(pattern)
for i in range(0, len(data_list)):
    line = data_list[i]

    if '主催者発行のもの' in line:
        date_row = data_list[i-2]
        place = date_row.split('ﾎﾞｰﾄﾚｰｽ')[1].replace('\n', '')
        print([date, place])

    if '電話投票締切予定' in line:
        raceNo = data_list[i].split('R')[0].replace(' ', '')
        st_row = i + 5 
        parse_data = []

        for ii in range (0, 6):
            racer = str(data_list[st_row+ii])
            print('racer = ', racer)

            value = re.match(pattern_re, racer).groups()
            print("value = ", value)
            list_value = list(value)
            list_value.insert(0, date)   # 日付
            list_value.insert(1, raceNo) # レースNo
            list_value.insert(2, place)  # 会場
            list_value.insert(17, 6.99)  # 展示タイム（ダミー）
            list_value.insert(18, 0.20)  # スタートタイム（ダミー）
            print("list_value = ", list_value)
            print()

            parse_data.append(list_value)
        i += 6

        oneday_df = pd.DataFrame(parse_data, columns=columns)
        all_place_data = pd.concat([all_place_data, oneday_df], axis=0)

        oneday_df.to_csv(f'./input/chokuzen/chokuzen_{place}_Race_{str(raceNo_b).zfill(2)}.csv')
        raceNo_b += 1
        if raceNo_b > 12:
            raceNo_b = 1

all_place_data.to_csv(f'./input/chokuzen/{date}.csv')
