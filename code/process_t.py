
import json
import uuid
import copy

filename = '../data/rotterdam/cityjson/t.json'
fin = open(filename)
j = json.loads(fin.read())
j2 = copy.deepcopy(j)


j2['extensions'] = {'NL3D': {'url': 'https://github.com/hugoledoux/nl3d/blob/master/schemas/extensions/nl_3d.json', 'version': '0.1'}}
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
    j2['CityObjects'][uid + '_k']['type'] = '+VegetatieObject'
    j2['CityObjects'][uid + '_k']['imgeo_type'] = 'boom'
    j2['CityObjects'][uid + '_k']['toplevel'] = True
    del j2['CityObjects'][uid + '_s']
    del j2['CityObjects'][uid + '_w']

json_str = json.dumps(j2, indent=2)
fout = open('../data/rotterdam/cityjson/t_nl3d.json', 'w')
fout.write(json_str)
print('Done.')

