import csv
import json
from collections import Counter

return_dict = {"nodes":[],"links":[]}

inner_links = {}
nodes = set()
connections = {}

ids = {}

id = 0
values = []
with open("input.csv") as f:
    for line in f.readlines():
        splitted_line = line.split(";")
        for name in splitted_line:
            if name not in nodes:
                id += 1

                inner_nodes = {"photo": "https://www.pinclipart.com/picdir/big/209-2098523_kids-sleeping-clip-art.png",
                               "size": 50, "info": "", 'name': name, 'id': id, 'group':id}
                ids.update({name:id})
                return_dict['nodes'].append(inner_nodes)
                nodes.add(name)

        splitted_line = line.split(";")
        values.append(ids[splitted_line[0]])
        inner_links = {"source": ids[splitted_line[0]], "target": ids[splitted_line[1]], "value": 2}
        return_dict['links'].append(inner_links)


for i in return_dict['nodes']:
    if i['id'] in values:
        i['size'] += 2 * values.count(i['id'])

#with open('output.json', 'w') as f:
#    json.dump(return_dict, f, ensure_ascii=False, indent=4)

print(json.dumps(return_dict,ensure_ascii=False, indent=4))

