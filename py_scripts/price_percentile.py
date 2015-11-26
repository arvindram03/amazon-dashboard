import json
from statistics import median
import numpy as np

rfile = "/Users/rhp/Documents/SBU/3Data Science/Course Project/reviewerid_prices.json"
wfile = "/Users/rhp/Documents/SBU/3Data Science/Course Project/reviewerid_prices_percentiles.csv"

r = open(rfile, 'r')
w = open(wfile, "w")

line = r.readline()
#count = 5
while line:
    l = json.loads(line)
    for k, v in l.iteritems():
        wl = k
        wl += "," + str(np.percentile(v, 25))
        wl += "," + str(np.percentile(v, 50))
        wl += "," + str(np.percentile(v, 75))
        wl += "," + str(len(v))
        wl += "\n"
        #print wl
    w.writelines(wl)
    # count -= 1
    # if count == 0:
    #     break
    line = r.readline()

r.close()