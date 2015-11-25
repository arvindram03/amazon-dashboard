import json

rfile = "/Users/rhp/Documents/SBU/3Data Science/Course Project/from_to_product.json"
wfile = "/Users/rhp/Documents/SBU/3Data Science/Course Project/product_data_graph_new.csv"

r = open(rfile, 'r')
w = open(wfile, 'w')

asin = {}
line = r.readline()
types = []
wl = "PID,Title,Price,SalesRank\n"
w.writelines(wl)
count = 0
while line:
    l = json.loads(line)
    count += 1
    if "asin" in l:
        if l["asin"] in asin:
            line = r.readline()
            continue
        asin[l["asin"]] = 1
        print count, len(asin)
        wl = str(l["asin"])

    if "title" in l:
        wl += "," + l["title"].replace(',', ';')
    else:
        wl += "," + "NULL"

    if "price" in l:
        wl += "," + str(l["price"])
    else:
        wl += "," + "0"

    if "salesRank" in l:
        if "Movies & TV" in l["salesRank"]:
            wl += "," + str(l["salesRank"]["Movies & TV"])
        else:
            wl += "," + "-1"
    else:
            wl += "," + "-1"

    wl += "\n"
    w.writelines(wl)
    # count -= 1
    # if not count:
    #     break
    # if "related" in l:
    #     for t in l["related"]:
    #         if t not in types:
    #             types.append(t)
    line = r.readline()

r.close()
w.close()
