import csv
import sys
import time

from datetime import datetime
from pytz import timezone

reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')

for row in reader:
    # Skip headers
    if len(row) > 1 and 'usage' in row[0]:
        if 'gas' in row[0]:
            # Gas is daily
            datetime_obj_naive = datetime.strptime(row[1], "%Y-%m-%d")
            datetime_obj_pacific = timezone('US/Pacific').localize(datetime_obj_naive)
            timestamp = time.mktime(datetime_obj_pacific.timetuple())

            print "energy,energy_type=gas,value_type=usage value=%s %s" % (row[2], timestamp)
            if row[4][1:] != "":
                print "energy,energy_type=gas,value_type=cost value=%s %s" % (row[4][1:], timestamp)
        else:
            # Electricity is hourly
            datetime_obj_naive = datetime.strptime(row[1] + " " + row[3], "%Y-%m-%d %H:%M")
            datetime_obj_pacific = timezone('US/Pacific').localize(datetime_obj_naive)
            timestamp = time.mktime(datetime_obj_pacific.timetuple())

            print "energy,energy_type=electric,value_type=usage value=%s %s" % (row[4], timestamp)
            if row[6][1:] != "":
                print "energy,energy_type=electric,value_type=cost value=%s %s" % (row[6][1:], timestamp)

        # print ', '.join(row)
