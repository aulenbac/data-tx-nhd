from pybis.nhd import Nhd as nhd
import requests
import json
from pprint import pprint
import sciencebasepy
import os

sb = sciencebasepy.SbSession()

username = input("Username:  ")
sb.loginc(str(username))

nhdRepositoryListings = requests.get('https://www.sciencebase.gov/catalog/items?parentId=5644f3c1e4b0aafbcd0188f1&filter=tags%3DNHDPlusV1&max=20&format=json&fields=files').json()

for item in nhdRepositoryListings['items']:
    thisFileName = item['id'] + '_SourceCatalog.json'
    nhdRepoCatalogURL = next((f['url'] for f in item['files'] if f['name'] == thisFileName), None)
    if nhdRepoCatalogURL is not None:
        thisCatalog = json.loads(requests.get(nhdRepoCatalogURL).text)
        sourceURL = 'ftp://'+thisCatalog['FTP Server']+'/'+thisCatalog['FTP Directory']

        for nhdFile in [item for item in thisCatalog['File Catalog'] if 'File Type' in item.keys() and item['File Type'].lower() == 'nhd']:
            if next((f for f in item['files'] if f['name'] == nhd.nhdv1_flowline_extract_filename(nhdFile['File Name'])), None) is None:
                sourcePath = sourceURL+nhdFile['File Name']
                extractFile = nhd.build_flowline_extract(sourcePath)
                sbItem = sb.get_item(item['id'])
                updatedItem = sb.upload_file_to_item(sbItem, extractFile)
                pprint(updatedItem['files'])
                os.remove(extractFile)

