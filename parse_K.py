import pandas as pd
from pathlib import Path
import re
import mojimoji
import logging

columns = {
    0: 'Date', 1: '会場', 2: 'Round', 3: '着順結果', 4: '艇番',
    5: '選手登番', 6: '選手名',
    7: 'モーターNo', 8: 'ボートNo', 9: '展示タイム', 10: '進入順位',
    11: 'スタートタイム', 12: 'レースタイム',
    13: '試合タイプ', 14: 'コース距離', 15: '天候', 16: '風向', 17: '風速', 18: '波高',
    19: '決まり手'
}

folder = Path('./input/boat_K/TXT/')
filepath = sorted(folder.glob('*.TXT'))
logging.info(filepath)

pattern = r'^(\w{2})([1-6])(\d{4})([^0-9]+)(\d{1,2})(\d{1,3})(\d{1}.\d{0,2})([1-6])(\d{0,1}.\d{0,2})(\d{0,1}.\d{0,2}.\d{0,1})'
pattern_re = re.compile(pattern)

for file in filepath:
    race_data_list = []
    date = file.stem.replace('K', '20')

    with file.open('r', encoding='shift_jis') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i]
        if 'KBGN' in line:
            ii = 1
            place = lines[i+1].split('［成績］')[0].replace('　', '')
            while True:
                line_ = lines[i+ii]
                if '----------' in line_:
                    logging.info('date = %s', date)
                    logging.info('place = %s', place)
                    rno = lines[i+ii-2].split('R')[0].replace('　', '').replace(' ', '')
                    kimarite = lines[i+ii-1].split('ﾚｰｽﾀｲﾑ ')[1].replace('　', '').replace('\n', '')

                    battle_type = lines[i+ii-2].split('R       ')[1].split('   ')[0].replace('　', '').replace(' ', '')
                    if '予選' in battle_type:
                        battle_type = '予選'
                    elif '準優勝戦' in battle_type:
                        battle_type = '準優勝戦'
                    elif '優勝戦' in battle_type:
                        battle_type = '優勝戦'
                    else:
                        battle_type = '一般戦'

                    battle_distance = lines[i+ii-2].split('H')[1].split('m  ')[0].replace('　', '')
                    weather = lines[i+ii-2].split('m  ')[1].split('  風')[0].replace('　', '')
                    wind_direction = lines[i+ii-2].split('風  ')[1].split('　')[0].replace('　', '')
                    wind_speed = lines[i+ii-2].split('風  ')[1].split('m  ')[0][-1]
                    nami_cm = lines[i+ii-2].split('波　')[1].split('cm')[0].replace('　', '').replace(' ', '')

                    logging.info(lines[i+ii+1])
                    logging.info('rno = %s', rno)
                    logging.info('kimarite = %s', kimarite)
                    logging.info('battle_type = %s', battle_type)
                    logging.info('battle_distance = %s', battle_distance)
                    logging.info('weather = %s', weather)
                    logging.info('wind_direction = %s', wind_direction)
                    logging.info('wind_speed = %s', wind_speed)
                    logging.info('nami_cm = %s', nami_cm)

                    for iii in range(1, 6+1):
                        racer_tmp = mojimoji.zen_to_han(lines[i+ii+iii]).replace(' ', '')
                        if ('K' not in racer_tmp) and ('F' not in racer_tmp) and ('L' not in racer_tmp):
                            logging.info('racer_tmp = %s', racer_tmp)
                            racer = re.match(pattern_re, racer_tmp).groups()
                            logging.info('racer = %s', racer)
                            try:
                                chakujun = int(racer[0].replace('0', ''))
                            except ValueError:
                                chakujun = 'NaN'
                            teiban = racer[1]
                            racer_toban = racer[2]
                            racer_name = racer[3]
                            motorNo = racer[4]
                            boatNo = racer[5]
                            tenji_time = racer[6]
                            shinnyuu_juni = racer[7]
                            start_time = racer[8]
                            race_time_tmp = racer[-1].split('.')
                            logging.info('race_time_tmp = %s', race_time_tmp)
                            if race_time_tmp[1] != '':
                                race_time = float(race_time_tmp[0]) * 60 + float(race_time_tmp[1]) + float(race_time_tmp[2]) * 0.1
                            else:
                                race_time = 'NaN'

                            logging.info('race_time = %s', race_time)
                            logging.info('')

                            race_data_list.append([date, place, rno, chakujun, teiban, racer_toban, racer_name,
                                                    motorNo, boatNo, tenji_time, shinnyuu_juni,start_time, race_time,
                                                    battle_type, battle_distance, weather, wind_direction, wind_speed, nami_cm,
                                                    kimarite])

                if 'KEND' in line_:
                    break

                ii += 1

        if 'FIN' in line:
            break
        i += 1

    logging.info(len(race_data_list))
    df = pd.DataFrame(race_data_list)

    new_all_df = df.rename(columns=columns)
    new_all_df.to_csv(f'./output_csv/out_K_{date}.csv', index=False)

logging.info('finished!')
