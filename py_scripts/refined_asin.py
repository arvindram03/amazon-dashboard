import json

rfile = "/Users/rhp/Documents/SBU/3Data Science/Course Project/movies-model-py.csv"

r = open(rfile, 'r')

line = r.readline()
asin = {}

while line:
    line = line.replace("\n", "")
    l = line.split(",")
    # print l
    if l[1] not in asin:
        asin[l[1]] = 1
    line = r.readline()

r.close()