import re
import pandas as pd
import glob
import os
import mojimoji

columns = ['Date', 'Round', '会場', '艇番', '選手登番', '選手名', '年齢', '支部', '体重', '級別', 
        '全国勝率', '全国２連率', '当地勝率', '当地２連率', 'モーター２連率', 'ボート２連率']

folder = './input/boat_B/TXT/'
filepath = glob.glob(folder + '*.TXT')
print(filepath)
for file in filepath:
    data_list = []
    oneday_df = pd.DataFrame(columns=columns)    
    with open(file, 'r', encoding='shift_jis') as f:
        data_list = f.readlines()
    
    data_list = [mojimoji.zen_to_han(line.replace('\u3000', '').replace('100.00', ' 99.99')) for line in data_list]
    
    parse_data = []
    pattern = r'^([1-6])\s(\d{4})(\D+)(\d{2})(\D+)(\d{2})([AB]\d{1})\s(\d{1}.\d{2})\s*(\d+.\d{2})\s(\d{1}.\d{2})\s*(\d+.\d{2})\s+\d+\s+(\d+.\d{2})\s*\d+\s+(\d+.\d{2})'
    pattern_re = re.compile(pattern)
    
    for i, line in enumerate(data_list):
        if '主催者発行のもの' in line:
            date_row = data_list[i-2]
            date = file.split('/')[-1].split('.TXT')[0].replace('B', '20').split('\\')[-1].replace('.txt', '')
            print("date = ", date)
            place = date_row.split('ﾎﾞｰﾄﾚｰｽ')[1].replace('\n', '')
            print([date, place])

        if '電話投票締切予定' in line:
            raceNo = line.split('R')[0].replace(' ', '')
            st_row = i + 5 
            exception_count = 0
            for ii in range(6):
                try:
                    racer = str(data_list[st_row+ii])
                    print(file)
                    print('racer = ', racer)
                    value = re.match(pattern_re, racer).groups()
                    print("value = ", value)
                    list_value = list(value)
                    list_value.insert(0, date)
                    list_value.insert(1, raceNo)
                    list_value.insert(2, place)
                    print("list_value = ", list_value)
                    print()
                    parse_data.append(list_value)
                except:
                    pass
    
    os.makedirs('./output_csv', exist_ok=True)
    output_filename = 'out_B_' + str(date) + '.csv'
    output_path = os.path.join('./output_csv', output_filename)

    oneday_df = pd.DataFrame(parse_data, columns=columns)
    oneday_df.to_csv(output_path, index=None)
    print("Saved file:", output_path)
