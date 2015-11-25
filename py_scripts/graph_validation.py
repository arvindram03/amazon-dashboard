import json

rfile = "/Users/rhp/Documents/SBU/3Data Science/Course Project/from_to_product.json"
also_bought = [
			"B000Z3N1HQ",
			"0578045427",
			"B007VI5AQ8",
			"B003AC98V2",
			"B004V4RW8O",
			"B000I0QL7I",
			"B000J10F8C",
			"B0007CEXYK",
			"B000ERVK4Y",
			"B000XSKDBA",
			"B002UNMWTC",
			"B00008MTXI",
			"B007TSV4GK",
			"B0052ADP6Y",
			"B00EUENWIY",
			"B003YKYX9M",
			"B004RD3YFE",
			"B007Y9F6RW",
			"B00004UEDQ",
			"B0039Y774Q",
			"B0006IIKRG",
			"B00JAGF9HE",
			"6305162026",
			"6305692572",
			"B001D7T460",
			"B0018QOIWG",
			"B002Y7ZELW",
			"B0045HCJ08",
			"0830907394",
			"B000LAZDPG",
			"B00A2H9QN8",
			"B001O5CLXY",
			"B000JBXXYK",
			"B003B3NGS6",
			"B0037SR3N4",
			"B00641Y2ZS",
			"0470903953",
			"0977977315",
			"B00049QQHI",
			"B000E6ESU8",
			"0470402741",
			"061565732X",
			"0615763146",
			"B000VZPTH8",
			"B003JO6OPO",
			"B00787BTEO",
			"B004R1Q7YQ",
			"B001GG6GKK",
			"B0015VQAZM",
			"1592854869",
			"B000QRIL08",
			"B000GQLA8O",
			"B000MPM3TE",
			"0979021804",
			"1608823407",
			"159285821X",
			"B00005Q4CS",
			"B0000549B1",
			"6305594333",
			"B00AFEXRME",
			"B004FN25AG",
			"0830906363",
			"0470402768",
			"1118414756",
			"B009SV4O2M",
			"1481106694",
			"1572306254",
			"B0013MOLPO",
			"B00009Y3QI",
			"B003NMOL2U",
			"B001AKBI8C",
			"0981708803",
			"1572306394",
			"B00B9LNPA6",
			"B005BYBZEK",
			"B004D7SBMU",
			"B00CQMADIO",
			"0470405511",
			"B00CHEHHT4",
			"B000ESUWY2",
			"0792838068",
			"B00AWE09Z0",
			"B00E4XZZEK",
			"0830914870",
			"B00GFZLEF4",
			"083090459X",
			"1402218443",
			"1893007170",
			"1893277046",
			"B005CKI7H6",
			"B0001LQL6K",
			"B000067S10",
			"0890425558",
			"B00114KYC8",
			"1466221224",
			"0943158508",
			"B00A7ID5BG",
			"0671765582",
			"B000B8IH10",
			"1568381395"
		]

also_viewed = [
			"B0036FO6SI",
			"B000KL8ODE",
			"000014357X",
			"B0037718RC",
			"B002I5GNVU",
			"B000RBU4BM"
		]

r = open(rfile, 'r')
# w = open(wfile, 'w')

asin = {}
line = r.readline()

count = 0
while line:
    l = json.loads(line)
    if "asin" in l:
        if l["asin"] in asin:
            line = r.readline()
            continue
        asin[l["asin"]] = 1
    # count -= 1
    # if not count:
    #     break
    line = r.readline()

r.close()

for id in also_viewed:
    if id in asin:
        count += 1

print count