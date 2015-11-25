import json
from statistics import median

rfile = "/Users/rhp/Documents/SBU/3Data Science/Course Project/reviewerid_prices.json"
wfile = "/Users/rhp/Documents/SBU/3Data Science/Course Project/reviewerid_prices_mean.csv"

r = open(rfile, 'r')
w = open(wfile, "w")

line = r.readline()
#count = 5
while line:
    l = json.loads(line)
    for k, v in l.iteritems():
        wl = k
        wl += "," + str(median(v))
        wl += "," + str(len(v))
        wl += "\n"
        #print wl
    w.writelines(wl)
    # count -= 1
    # if count == 0:
    #     break
    line = r.readline()

r.close()