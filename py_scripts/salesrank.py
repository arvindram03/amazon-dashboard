import json

rfile = "/Users/rhp/Documents/SBU/3Data Science/Course Project/salesRank.json"
wfile = "/Users/rhp/Documents/SBU/3Data Science/Course Project/movies_salesrank_extract.csv"

r = open(rfile, 'r')
w = open(wfile, 'w')

line = r.readline()
#line = "{'asin': '0000143561', 'categories': [['Movies & TV', 'Movies']], 'description': '3Pack DVD set - Italian Classics, Parties and Holidays.', 'title': 'Everyday Italian (with Giada de Laurentiis), Volume 1 (3 Pack): Italian Classics, Parties, Holidays', 'price': 12.99, 'salesRank': {'Movies & TV': 376041}, 'imUrl': 'http://g-ecx.images-amazon.com/images/G/01/x-site/icons/no-img-sm._CB192198896_.gif', 'related': {'also_viewed': ['B0036FO6SI', 'B000KL8ODE', '000014357X', 'B0037718RC', 'B002I5GNVU', 'B000RBU4BM'], 'buy_after_viewing': ['B0036FO6SI', 'B000KL8ODE', '000014357X', 'B0037718RC']}}"
#line = line.replace("\'", "\"")
#l = json.loads(line)

sr = []

count = 5
while line:
    l = json.loads(line)
    if "asin" in l:
        wl = str(l["asin"])
    else:
        wl = ""

    if "title" in l:
        wl += "," + '"' + l["title"].replace(",", "") + '"'
    else:
        wl += "," + ""

    if "price" in l:
        wl += "," + str(l["price"])
    else:
        wl += "," + "-1"

    if "salesRank" in l:
        for cat in l["salesRank"]:
            if cat not in sr:
                sr.append(cat)
        if "Movies & TV" in l["salesRank"]:
            wl += "," + str(l["salesRank"]["Movies & TV"])
        elif "Movies" in l["salesRank"]:
            wl += "," + str(l["salesRank"]["Movies"])
        elif "TV" in l["salesRank"]:
            wl += "," + str(l["salesRank"]["TV"])
        else:
            wl += "," + ""
    else:
        wl += "," + ""

    wl += "\n"
    #print wl
    line = r.readline()
    #w.writelines(wl)

r.close()
w.close()

print sr