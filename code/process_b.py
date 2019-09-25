
import json
import uuid
import copy

filename = '../data/rotterdam/cityjson/b.json'
fin = open(filename)
j = json.loads(fin.read())
j2 = copy.deepcopy(j)


j2['extensions'] = {'NL3D': {'url': 'https://github.com/hugoledoux/nl3d/blob/master/schemas/extensions/nl_3d.json', 'version': '0.1'}}
j2['metadata']['referenceSystem'] = 'urn:ogc:def:crs:EPSG::7415'

j2['@context'] = []
j2['@context'].append("http://localhost:8080/contexts/context_imgeo.jsonld")
j2['@context'].append("http://localhost:8080/contexts/context_cityjson.jsonld")


for cid in j['CityObjects']:
    co = j['CityObjects'][cid]
    if (co['type'] == 'Building'):
        j2['CityObjects'][cid]['type'] = '+Pand'
        j2['CityObjects'][cid]['@context'] = 'https://bag.basisregistraties.overheid.nl/bag/id/pand/' + cid[3:]
        if 'children' in j['CityObjects'][cid]:
            for childid in j['CityObjects'][cid]['children']:
                for each in j['CityObjects'][childid]['geometry']:
                    j2['CityObjects'][cid]['geometry'].append(each)

#-- delete BuildingPart and BuildingInstallation
lsids = []
for cid in j2['CityObjects']:
    co = j2['CityObjects'][cid]
    if (co['type'] == 'BuildingInstallation'):
        lsids.append(cid)
    if (co['type'] == 'BuildingPart'):
        lsids.append(cid)
for each in lsids:
    del j2['CityObjects'][each]


json_str = json.dumps(j2, indent=2)
fout = open('tmp.json', 'w')
fout.write(json_str)
print('Done: tmp.json saved.')

