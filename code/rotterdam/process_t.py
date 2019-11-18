
import json
import uuid
import copy

filename = '../data/rotterdam/cityjson/t.json'
fin = open(filename)
j = json.loads(fin.read())
j2 = copy.deepcopy(j)



j2['metadata']['referenceSystem'] = 'urn:ogc:def:crs:EPSG::7415'

j2['@context'] = []
j2['@context'].append("http://localhost:8080/contexts/context_imgeo.jsonld")
j2['@context'].append("http://localhost:8080/contexts/context_cityjson.jsonld")

uids = set()
for cid in j['CityObjects']:
    pos = cid.rfind('_')
    uids.add(cid[:pos])
# print(uids)

for uid in uids:
    j2['CityObjects'][uid + '_k']['geometry'].append(j2['CityObjects'][uid + '_s']['geometry'][0])
    j2['CityObjects'][uid + '_k']['geometry'].append(j2['CityObjects'][uid + '_w']['geometry'][0])
    j2['CityObjects'][uid + '_k']['type'] = 'SolitaryVegetationObject'
    j2['CityObjects'][uid + '_k']['attributes']['class'] = {}
    j2['CityObjects'][uid + '_k']['attributes']['class'] = "VegetatieObject"
    j2['CityObjects'][uid + '_k']['attributes']['function'] = "Boom"
    del j2['CityObjects'][uid + '_s']
    del j2['CityObjects'][uid + '_w']

json_str = json.dumps(j2)
fout = open('../data/rotterdam/cityjson/t_nl3d.json', 'w')
fout.write(json_str)
print('Done.')

