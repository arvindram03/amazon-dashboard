import json
from py2neo import Graph, authenticate, neo4j

authenticate("localhost:7474", "neo4j", "password")
f = ['B000M66HHW', 'B0010358CQ', 'B0007939U2', 'B000A2WQUA', 'B000VKJ6Y0', 'B000M66HHW']
t = ['B000M66HHW', 'B000VKJ6Y0', 'B003ZQQXH0', 'B000UMP2VK', 'B000VBJEEG', 'B000ROAK2W']
res = []
g = Graph()

min_len = -1

for i in xrange(len(f)):
    for j in xrange(len(t)):
        query = "MATCH (from:Product { pid:'" + f[i] + "' }), (to:Product { pid: '" + t[j] + "'}) , path = shortestPath(from-[:TO*]->to ) RETURN path"
        results = g.cypher.execute(query)
        path_len = len(str(results).split(":TO")) - 1
        print f[i], t[j], path_len
        if min_len == -1 or path_len < min_len:
            min_len = path_len

    if min_len < 5:
        res.append(f[i])
    min_len = -1

print res
# print min_len
