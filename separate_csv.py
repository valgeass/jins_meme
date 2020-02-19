import pandas as pd
import datetime

class SeparateCsv():
    def __init__(self, date):
      self.date = date
      self.df = pd.read_csv('./output/csv/{0}/all_{0}.csv'.format(self.date))
      self.count = 1
      self.separate_array = [0]
    def separate_csv(self):
      self.df['date'] = pd.to_datetime(self.df['date'])
      for i in range(len(self.df) - 1):
          if (self.df['date'][i + 1] - self.df['date'][i]).seconds >= 3600:
            self.count += 1
            self.separate_array.append(i+1)
      for i in range(self.count-1):
          self.df.iloc[self.separate_array[i]:self.separate_array[i + 1]].to_csv('./output/csv/{0}/separate_{0}_{1}.csv'.format(self.date, i+1), index=False)
          if i == self.count - 2:
            self.df.iloc[self.separate_array[i+1]:len(self.df)].to_csv('./output/csv/{0}/separate_{0}_{1}.csv'.format(self.date, self.count), index=False)