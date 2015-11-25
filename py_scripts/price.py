import json

rfile = "/Users/rhp/Documents/SBU/3Data Science/Course Project/asin_price.json"
r2file = "/Users/rhp/Documents/SBU/3Data Science/Course Project/review_order.json"
wfile = "/Users/rhp/Documents/SBU/3Data Science/Course Project/reviewerid_prices.json"

r = open(rfile, 'r')
#
exit(0)
price_dict = {}

line = r.readline()

while line:
    l = json.loads(line)
    if "price" in l:
        price_dict[l["asin"]] = l["price"]
    else:
        price_dict[l["asin"]] = 0
    line = r.readline()

r.close()

r = open(r2file, 'r')
w = open(wfile, 'w')
pl = []
line = r.readline()
# prev = json.loads(line)["reviewerID"]
# pl.append(price_dict[json.loads(line)["asin"]])
# wl = {}
# wl[prev] = pl
prev = ""
wl = {}
wlines = ""
count = 50
while line:
    l = json.loads(line)
    curr = l["reviewerID"]

    if len(prev) == 0:
        prev = curr

    if prev != curr:
        wl[prev] = pl
        pl = []
        pl.append(price_dict[l["asin"]])
        wlines = json.dumps(wl)
        wlines += "\n"
        w.writelines(wlines)
        wl = {}
    else:
        pl.append(price_dict[l["asin"]])

    prev = curr
    # if not count:
    #     break
    line = r.readline()

#print wl
r.close()
w.close()

