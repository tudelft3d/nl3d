
import json
import uuid
import copy

filename = '../data/rotterdam/cityjson/cf.json'
fin = open(filename)
j = json.loads(fin.read())
j2 = copy.deepcopy(j)

j2['metadata']['referenceSystem'] = 'urn:ogc:def:crs:EPSG::7415'

j2['@context'] = []
j2['@context'].append("http://localhost:8080/contexts/context_imgeo.jsonld")
j2['@context'].append("http://localhost:8080/contexts/context_cityjson.jsonld")


for cid in j['CityObjects']:
    if 'Lamp_id' in j['CityObjects'][cid]['attributes']:
        lampid = j['CityObjects'][cid]['attributes']['Lamp_id']
        for cid2 in j['CityObjects']:
            if 'Odg_lamp_id' in j['CityObjects'][cid2]['attributes']:
                if j['CityObjects'][cid2]['attributes']['Odg_lamp_id'] == lampid:
                    j2['CityObjects'][cid]['geometry'].append(j['CityObjects'][cid2]['geometry'][0])
                    j2['CityObjects'][cid]['type'] = 'CityFurniture'
                    j2['CityObjects'][cid]['attributes']['class'] = "Paal"
                    j2['CityObjects'][cid]['attributes']['function'] = "Lichtmast"
                    del j2['CityObjects'][cid2]



# for uid in uids:
#     j2['CityObjects'][uid + '_k']['geometry'].append(j2['CityObjects'][uid + '_s']['geometry'][0])
#     j2['CityObjects'][uid + '_k']['geometry'].append(j2['CityObjects'][uid + '_w']['geometry'][0])
#     j2['CityObjects'][uid + '_k']['type'] = '+VegetatieObject'
#     j2['CityObjects'][uid + '_k']['toplevel'] = True
#     del j2['CityObjects'][uid + '_s']
#     del j2['CityObjects'][uid + '_w']

json_str = json.dumps(j2)
fout = open('../data/rotterdam/cityjson/cf_nl3d.json', 'w')
fout.write(json_str)
print('Done.')

