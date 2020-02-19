import argparse
import jins_api_auth
import make_csv
import json
import os
import datetime
import pandas as pd
import shutil
import separate_csv

parser = argparse.ArgumentParser(description='jins_id')
parser.add_argument('--input_id', '-i', required=True)
parser.add_argument('--input_secret', '-s', required=True)
parser.add_argument('--date', '-d', default='19700101', type=str)

args = parser.parse_args()
ID = args.input_id
SECRET = args.input_secret
DATE = args.date

def output_json(json_data):
    if not os.path.exists('./output/json/'):
        os.makedirs('./output/json/')
    json_path = './output/json/jins_data_{}.json'.format(DATE[0:8])
    with open(json_path, 'w') as f:
        json.dump(json.loads(json_data), f, indent=4)
    return json_path

def output_csv(json_path, DATE, time_count):
    if not os.path.exists('./output/csv/{}'.format(DATE)):
        os.makedirs('./output/csv/{}'.format(DATE))
    csv_init = make_csv.MakeCsv(json_path, DATE, time_count)
    csv_init.make_csv()

def merge_csv(date):
    output_path = './output/csv/{0}'.format(date)
    path = os.listdir(output_path)
    merge_df = pd.read_csv('./output/csv/{0}/'.format(date) + path[0])
    for index, file_path in enumerate(path):
        try:
            df = pd.read_csv('./output/csv/{0}/'.format(date) + file_path).dropna()
            merge_df = pd.merge(merge_df, df, on=['date', 'zone', 'focus', 'calm', 'posture', 'bki_sum', 'bki_n'], how='outer', )
        except Exception as e:
            pass
    merge_df.sort_values('date', inplace=True)
    shutil.rmtree(output_path)
    os.mkdir(output_path)
    try:
        for i in range(len(merge_df)):
            date_timezone= pd.to_datetime(merge_df['date'])
            merge_df['date'][i] = date_timezone[i].tz_convert(None) + datetime.timedelta(hours=9)
    except Exception as e:
        pass
    merge_df.to_csv('./output/csv/{0}/all_{0}.csv'.format(date), index=False)

if __name__ == "__main__":
    if (len(DATE) == 8):
        if not os.path.isdir('./output/csv/{}'.format(DATE)):
            time_count = datetime.datetime(1, 1, 1, 0, 29, 0)
            for i in range(48):
                token = jins_api_auth.GetAllowCode(ID, SECRET, DATE)
                code = token.login_url()
                jins_info = token.get_access_token(code, time_count)
                json_path = output_json(jins_info)
                output_csv(json_path, DATE, time_count)
                time_count += datetime.timedelta(minutes=30)
            merge_csv(DATE)
            separate_csv = separate_csv.SeparateCsv(DATE)
            separate_csv.separate_csv()
    else:
        print('input date yyyymmdd')
