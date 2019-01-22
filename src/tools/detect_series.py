import db
import os
import shutil
from datetime import datetime

def remove_single_entries(series):
    return ([x for x in series if len(x) > 3], [x[0] for x in series if len(x) <= 3])

def detect_series(pictures_by_datetime):
    last_datetime = None
    series = []
    current_series = []
    for pic in pictures_by_datetime:
        if last_datetime == None:
            current_series = [pic]
            series.append(current_series)
        else:
            if (pic[0] - last_datetime).total_seconds() > 4:
                # The pictures are not taken within less than 5 seconds, so
                # start a new series now:
                current_series = [pic]
                series.append(current_series)
            else:
                # The pictures is taken less than 5 seconds after the previous
                # one, so add it to the series:
                current_series.append(pic)
        last_datetime = pic[0]
    return remove_single_entries(series)

(series, singleshots) = detect_series(db.load_db('photos.db', db.PicturesSort.by_date_time))

target_path = '.\\SampleOutput\\'

for x in series:
    series_no = x[0][0].strftime('%Y-%m-%d-%H-%M-%S')
    series_path = os.path.abspath(os.path.join(target_path, series_no))
    if not(os.path.isdir(series_path) and os.path.exists(series_path)):
        os.makedirs(series_path)
    for pic in x:
        target_file = os.path.join(series_path, os.path.basename(pic[1]))
        print('Copying {0} to {1}'.format(pic[1], target_file))
        shutil.copyfile(pic[1], target_file)

