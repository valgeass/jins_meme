import json
import csv
import config
import datetime
import os

JINS_COLUMNS = config.JINS_API_COLUMNS

class MakeCsv():
    def __init__(self, json_path, date, time_count):
        self.json_path = json_path
        self.json_dict = json.load(open(self.json_path, 'r'))
        self.json_dicts = self.json_dict['computed_data']
        self.date = date
        self.time_count = str(time_count.hour) + str(time_count.minute) + str(time_count.second)

    def make_csv(self):
        for json_compute in self.json_dict['computed_data']:
            for json_col in range(len(self.json_dict['computed_data'][json_compute])):
                map_list = map(lambda x: self.json_dict['computed_data'][json_compute][json_col][x], JINS_COLUMNS)
        with open('./output/csv/{0}/data_{0}_{1}.csv'.format(self.date, self.time_count), 'w') as f:
            csv.register_dialect('dialect01', doublequote=True, quoting=csv.QUOTE_ALL)
            writer = csv.DictWriter(f, fieldnames=config.JINS_API_COLUMNS, dialect='dialect01')
            writer.writeheader()
            for target_dict in self.json_dicts:
                for columns in self.json_dicts[target_dict]:
                    writer.writerow(columns)

