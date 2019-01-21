from __future__ import print_function
import exifread
import filetype
import os
import time
import sqlite3
from enum import Enum
from datetime import datetime

def build_db(root_dir, db_file):
    i = 0
    pictures = dict()
    sql_con = sqlite3.connect(db_file)
    sql_find = sql_con.cursor()
    sql_insert = sql_con.cursor()

    try:
        file_names = []
        for root, dirs, files in os.walk(root_dir):
            for file_base_name in files:
                upper = file_base_name.upper()
                if upper.endswith('JPEG') or upper.endswith('JPG'):
                    file_names.append(os.path.join(root, file_base_name))

        i_max = len(file_names)
        last_percent = 0
        print(i_max)
        for file_name in file_names:
            sql_find.execute('select file_path from photos where file_path=?', (file_name,))
            if sql_find.fetchone() == None:
                with open(file_name, 'rb') as f:
                    exif = exifread.process_file(f)
                    if 'EXIF DateTimeOriginal' in exif:
                        date_time_str = str(exif['EXIF DateTimeOriginal'])
                        date_time = time.strptime(date_time_str, '%Y:%m:%d %H:%M:%S')
                        pictures[file_name] = date_time
                        sql_insert.execute('insert into photos(file_path, datetime)values(?, ?)', (file_name, datetime.fromtimestamp(time.mktime(date_time))))
                        sql_con.commit()
            i = i + 1
            cur_percent = int(float(i) / float(i_max) * 100.)
            if cur_percent != last_percent:
                last_percent = cur_percent
                print('{cur_percent}%'.format(cur_percent=cur_percent))
    except KeyboardInterrupt:
        pass

    sql_find.close()
    sql_insert.close()
    sql_con.commit()
    return pictures

class PicturesSort(Enum):
    by_photo_path = 1,
    by_date_time = 2

def load_db(db_file, sort_by = PicturesSort.by_photo_path):
    sql_con = sqlite3.connect(db_file)
    sql_find = sql_con.cursor()
    sql_find.execute('select file_path, datetime from photos')
    pictures = dict()
    datetimes = []
    while True:
        row = sql_find.fetchone()
        if row == None:
            break
        else:
            row = (row[0], datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S'))
            if sort_by == PicturesSort.by_photo_path:
                pictures[row[0]] = row[1]
            else:
                datetimes.append((row[1], row[0]))
    if sort_by == PicturesSort.by_photo_path:
        return pictures
    else:
        return sorted(datetimes, key=lambda x: x[0])

