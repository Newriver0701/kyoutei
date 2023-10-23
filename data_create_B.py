import re
import pandas as pd
import glob
import os
import multiprocessing

os.makedirs('./output_csv_all', exist_ok=True)

place_mapper = {
    '桐生': 1, '戸田': 2, '江戸川': 3, '平和島': 4, '多摩川': 5,
    '浜名湖': 6, '蒲郡': 7, '常滑': 8, '津': 9, '三国': 10,
    'びわこ': 11, '住之江': 12, '尼崎': 13, '鳴門': 14, '丸亀': 15,
    '児島': 16, '宮��': 17, '徳山': 18, '下関': 19, '若松': 20,
    '芦屋': 21, '福岡': 22, '唐津': 23, '大村': 24
}

columns = [
    'Date', 'Round', '会場',
    '選手登番_1', '選手登番_2', '選手登番_3', '選手登番_4', '選手登番_5', '選手登番_6',
    '選手名_1', '選手名_2', '選手名_3', '選手名_4', '選手名_5', '選手名_6',
    '年齢_1', '年齢_2', '年齢_3', '年齢_4', '年齢_5', '年齢_6',
    '支部_1', '支部_2', '支部_3', '支部_4', '支部_5', '支部_6',
    '体重_1', '体重_2', '体重_3', '体重_4', '体重_5', '体重_6',
    '級別_1', '級別_2', '級別_3', '級別_4', '級別_5', '級別_6',
    '全国勝率_1', '全国勝率_2', '全国勝率_3', '全国勝率_4', '全国勝率_5', '全国勝率_6',
    '全国2連率_1', '全国2連率_2', '全国2連率_3', '全国2連率_4', '全国2連率_5', '全国2連率_6',
    '当地勝率_1', '当地勝率_2', '当地勝率_3', '当地勝率_4', '当地勝率_5', '当地勝率_6',
    '当地2連率_1', '当地2連率_2', '当地2連率_3', '当地2連率_4', '当地2連率_5', '当地2連率_6',
    'モーター2連率_1', 'モーター2連率_2', 'モーター2連率_3', 'モーター2連率_4', 'モーター2連率_5', 'モーター2連率_6',
    'ボート2連率_1', 'ボート2連率_2', 'ボート2連率_3', 'ボート2連率_4', 'ボート2連率_5', 'ボート2連率_6',
    '結果_1着', '結果_2着', '結果_3着',
    '決まり手', '払戻金'
]

payout_pattern = '(\s+)(\d{1,2}R)(\s+)(\d-\d-\d)(\s+)(\d{3,6})(\s+)'


def worker_B(args):
    no, filepath = args
    df_output_all = pd.DataFrame()
    for filename in filepath:
        df = pd.read_csv(filename)
        for i in range(0, len(df), 6):
            df_output = pd.DataFrame()
            df_one_race = df[i:i + 6].reset_index()

            date = pd.DataFrame([df_one_race['Date'][0]])
            race = pd.DataFrame([df_one_race['Round'][0]])
            place = pd.DataFrame([df_one_race['会場'][0]])
            for key, value in place_mapper.items():
                if str(key) == str(place.iat[0, 0]):
                    placeNo = value
                    break

            df_output = pd.concat([df_output, date, race, place], axis=0)

            data_toban = df_one_race['選手登番']
            data_name = df_one_race['選手名']
            data_age = df_one_race['年齢']
            data_shibu = df_one_race['支部']
            data_weight = df_one_race['体重']
            data_kyubetsu = df_one_race['級別']
            data_zenkoku_shoritsu = df_one_race['全国勝率']
            data_zenkoku_2ren = df_one_race['全国２連率']
            data_touchi_shouritsu = df_one_race['当地勝率']
            data_touchi_2ren = df_one_race['当地２連率']
            data_motor_2ren = df_one_race['モーター２連率']
            data_boat_2ren = df_one_race['ボート２連率']

            K_filename = filename.split('out_B_20')[1].split('.csv')[0]
            K_path = 'input/boat_K/TXT/K' + K_filename + '.TXT'
            with open(K_path, 'r', encoding='shift_jis') as f:
                lines = f.readlines()
            j = 1
            while True:
                line = lines[j]
                if str(placeNo).zfill(2) + 'KBGN\n' == line:
                    for jj in range(j, len(lines)):
                        try:
                            result = lines[jj].split(str(race.iat[0, 0]) + 'R  ')[1].split(' ')[0]
                            payout = re.match(payout_pattern, str(lines[jj])).groups()[-2]
                        except:
                            pass
                        else:
                            break

                    for jj in range(j, len(lines)):
                        if '--------------' in lines[jj]:
                            rno = lines[jj - 2].split('R  ')[0].replace(' ', '')
                        else:
                            rno = None

                        if rno == str(race.iat[0, 0]):
                            kimarite = lines[jj - 1].split(' ﾚｰｽﾀｲﾑ ')[1].split('　')[0].replace('\n', '').replace('"', '')
                            break

                if str(placeNo).zfill(2) + 'KEND\n' == line:
                    break
                j += 1

            try:
                data_1chaku = pd.DataFrame([result.split('-')[0]])
                data_2chaku = pd.DataFrame([result.split('-')[1]])
                data_3chaku = pd.DataFrame([result.split('-')[2]])
                data_kimarite = pd.DataFrame([kimarite])
                data_payout = pd.DataFrame([payout])

                df_output = pd.concat([df_output, data_toban, data_name, data_age, data_shibu, data_weight, data_kyubetsu,
                                       data_zenkoku_shoritsu, data_zenkoku_2ren,
                                       data_touchi_shouritsu, data_touchi_2ren,
                                       data_motor_2ren, data_boat_2ren,
                                       data_1chaku, data_2chaku, data_3chaku,
                                       data_kimarite,
                                       data_payout], axis=0).T

                sh = df_output.shape
                df_output.columns = range(sh[1])
                df_output_all = pd.concat([df_output_all, df_output], axis=0)
                df_output_all_new = df_output_all.rename(columns=dict(enumerate(columns)))

                df_output_all_new.to_csv('./output_csv_all/Bout_' + str(no) + '.csv', index=None)

            except:
                pass


if __name__ == '__main__':
    filepath_B = sorted(glob.glob('./output_csv/out_B_*.csv'))
    file_count = len(filepath_B)
    process_num = 13
    files_per_process = 30

    with multiprocessing.Pool(processes=process_num) as pool:
        pool.map(worker_B, [(no, filepath_B[(no - 1) * files_per_process:no * files_per_process]) for no in range(1, process_num + 1)])
