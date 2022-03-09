import pandas as pd
import csv
import re

# file paths
data = 'fb_data.csv'
labels = 'fb_label.csv'

with open('fb_label.csv', 'r') as infile:
    with open('clean_fb_label.csv', 'w') as outfile:
        writer = csv.writer(outfile)
        labelreader = csv.reader(infile)
        for row in labelreader:
            if row[0]:
                writer.writerow(row)

df1 = pd.read_csv('fb_data.csv')
df2 = pd.read_csv('clean_fb_label.csv')
pd.concat([df1, df2], axis = 1).to_csv('fbcombined.csv', index=False)

