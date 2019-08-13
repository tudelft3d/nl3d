
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
        #-- case 1
        if ('children' not in co):
            # print ('NO children')
            j2['CityObjects'][cid]['type'] = '+Pand'
            newid = str(uuid.uuid4())
            j2['CityObjects'][newid] = {'type': '+Gebouw'}
            j2['CityObjects'][newid]['geometry'] = []
            j2['CityObjects'][newid]['children'] = [cid]
            j2['CityObjects'][cid]['parents'] = [newid]
            j2['CityObjects'][newid]['address'] = j['CityObjects'][cid]['address']        
            del j2['CityObjects'][cid]['address']

        #-- case 2: has children
        else:
            # print(cid)
            if len(j['CityObjects'][cid]['geometry']) == 0:
                j2['CityObjects'][cid]['type'] = '+Gebouw'
                if 'children' in j['CityObjects'][cid]: 
                    for childid in j['CityObjects'][cid]['children']:
                        if (j2['CityObjects'][childid]['type'] == 'BuildingPart'):
                            j2['CityObjects'][childid]['type'] = '+Pand'
                        elif (j2['CityObjects'][childid]['type'] == 'BuildingInstallation'):
                            j2['CityObjects'][childid]['type'] = '+PandInstallatie'
                            # j2['CityObjects'][childid]['parents'] = [c]
            else:
                j2['CityObjects'][cid]['type'] = '+Pand'
                newid = str(uuid.uuid4())
                j2['CityObjects'][newid] = {'type': '+Gebouw'}
                j2['CityObjects'][newid]['geometry'] = []
                j2['CityObjects'][newid]['children'] = [cid]
                j2['CityObjects'][cid]['parents'] = [newid]
                j2['CityObjects'][newid]['address'] = j['CityObjects'][cid]['address']        
                del j2['CityObjects'][cid]['address']
                if 'children' in j['CityObjects'][cid]: 
                    for childid in j['CityObjects'][cid]['children']:
                        if (j2['CityObjects'][childid]['type'] == 'BuildingPart'):
                            j2['CityObjects'][childid]['type'] = '+Pand'
                        elif (j2['CityObjects'][childid]['type'] == 'BuildingInstallation'):
                            j2['CityObjects'][childid]['type'] = '+PandInstallatie'
                            j2['CityObjects'][childid]['parents'] = [cid]
    

    
    # if (co['type'] == 'BuildingPart'):
    #     if ('parents' not in co):
    #         print('->', cid)
    #     else:
    #         print(cid)

for cid in j2['CityObjects']:
    co = j2['CityObjects'][cid]
    if (co['type'] == 'BuildingInstallation'):
        j2['CityObjects'][cid]['type'] = '+PandInstallatie'

for cid in j2['CityObjects']:
    co = j2['CityObjects'][cid]
    if (co['type'] == '+Gebouw'):
        j2['CityObjects'][cid]['toplevel'] = True
    else:
        j2['CityObjects'][cid]['toplevel'] = False



json_str = json.dumps(j2, indent=2)
fout = open('tmp.json', 'w')
fout.write(json_str)

