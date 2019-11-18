
import json
import uuid
import copy

filename = '/Users/hugo/Dropbox/data/cityjson/tudelft-campus/tudelft_campus.json'
fin = open(filename)
j = json.loads(fin.read())

j['@context'] = []
j['@context'].append("http://localhost:8080/contexts/context_imgeo.jsonld")
j['@context'].append("http://localhost:8080/contexts/context_cityjson.jsonld")

for cid in j['CityObjects']:
    co = j['CityObjects'][cid]
    # Building
    if (co['type'] == 'Building'):
        j['CityObjects'][cid]['attributes']['class'] = "Pand"
        bagid = j['CityObjects'][cid]['attributes']['identificatiebagpnd']
        if len(bagid) == 15:
            bagid = '0' + bagid
        j['CityObjects'][cid]['@context'] = 'https://bag.basisregistraties.overheid.nl/bag/id/pand/' + bagid

    # Bridge
    if (co['type'] == 'Bridge'):
        j['CityObjects'][cid]['attributes']['class'] = "Overbruggingsdeel"
        j['CityObjects'][cid]['attributes']['function'] = j['CityObjects'][cid]['attributes']['typeoverbruggingsdeel']

    # GenericCityObject
    if (co['type'] == 'GenericCityObject'):
        # j['CityObjects'][cid]['attributes']['class'] = "Waterdeel"
        # TODO : how to fetch the correct IMGeo type? 
        j['CityObjects'][cid]['attributes']['function'] = j['CityObjects'][cid]['attributes']['bgt-type']

    # LandUse
    if (co['type'] == 'LandUse'):
        j['CityObjects'][cid]['attributes']['class'] = "OnbegroeidTerreindeel"
        j['CityObjects'][cid]['attributes']['function'] = j['CityObjects'][cid]['attributes']['bgt-fysiekvoorkomen']

    # PlantCover
    if (co['type'] == 'PlantCover'):
        j['CityObjects'][cid]['attributes']['class'] = "BegroeidTerreindeel"
        j['CityObjects'][cid]['attributes']['function'] = j['CityObjects'][cid]['attributes']['bgt-fysiekvoorkomen']

    # Road
    if (co['type'] == 'Road'):
        j['CityObjects'][cid]['attributes']['class'] = "Wegdeel"
        j['CityObjects'][cid]['attributes']['function'] = j['CityObjects'][cid]['attributes']['bgt-fysiekvoorkomen']

    # WaterBody
    if (co['type'] == 'WaterBody'):
        j['CityObjects'][cid]['attributes']['class'] = "Waterdeel"
        j['CityObjects'][cid]['attributes']['function'] = j['CityObjects'][cid]['attributes']['bgt-type']


json_str = json.dumps(j)
fout = open('/Users/hugo/temp/tud_nl3d.json', 'w')
fout.write(json_str)
print('Done.')

