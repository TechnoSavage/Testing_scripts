#!/usr/bin/python

import csv
import json

with open('hw_fields_public.json') as jf:
    assets = json.load(jf)

cf = open('hw_fields_public.csv', 'w')

csv_writer = csv.writer(cf)

count = 0

for asset in assets:
    if count == 0:
        header = asset.keys()
        csv_writer.writerow(header)
        count += 1

    csv_writer.writerow(asset.values())

cf.close()