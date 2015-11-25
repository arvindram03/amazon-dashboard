import json

r0file = "/Users/rhp/Documents/SBU/3Data Science/Course Project/movies-model-py.csv"
rfile = "/Users/rhp/Documents/SBU/3Data Science/Course Project/from_to_product.json"
wfile = "/Users/rhp/Documents/SBU/3Data Science/Course Project/product_product_relation.csv"
err = "/Users/rhp/Documents/SBU/3Data Science/Course Project/product_not_found.txt"

r = open(r0file, 'r')
# w = open(wfile, 'w')

asin = {}
line = r.readline()

count = 0
# while line:
#     l = json.loads(line)
#     if "asin" in l:
#         if l["asin"] in asin:
#             line = r.readline()
#             continue
#         asin[l["asin"]] = 0
#     # count -= 1
#     # if not count:
#     #     break
#     line = r.readline()
while line:
    line = line.replace("\n", "")
    l = line.split(",")
    # print l
    if l[1] not in asin:
        asin[l[1]] = 0
    line = r.readline()

r.close()

r = open(rfile, 'r')
w = open(wfile, 'w')
e = open(err, 'w')

line = r.readline()
wl = "From,Type,To\n"
w.writelines(wl)
el = ""
count = 1
while line:
    l = json.loads(line)
    el = ""
    wl = ""
    if "related" in l:
        if "also_bought" in l["related"]:
            for pid in l["related"]["also_bought"]:
                if pid not in asin:
                    el += str(pid) + "\tBOUGHT" + "\n"
                else:
                    wl += str(l["asin"])
                    wl += "," + "BOUGHT" + "," + str(pid) + "\n"
        if "also_viewed" in l["related"]:
            for pid in l["related"]["also_viewed"]:
                if pid not in asin:
                    el += str(pid) + "\tVIEWED" + "\n"
                else:
                    wl += str(l["asin"])
                    wl += "," + "VIEWED" + "," + str(pid) + "\n"
    if l["asin"] in asin:
        if asin[l["asin"]] == 0:
            asin[l["asin"]] = 1
            w.writelines(wl)
            e.writelines(el)
    # count += 1
    # print count
    line = r.readline()

r.close()
w.close()
e.close()