from functions import Nhd as nhd
import requests
import json
import sciencebasepy
import os

sb = sciencebasepy.SbSession()

username = input("Username:  ")
sb.loginc(str(username))

nhdRepositoryListings = requests.get('https://www.sciencebase.gov/catalog/items?filter=tags%3DNHDPlusV1&max=20&format=json&fields=webLinks').json()

for item in nhdRepositoryListings['items']:
    nhdRepoLink = next((wl['uri'] for wl in item['webLinks'] if wl['typeLabel'] == 'Source Repository'), None)
    if nhdRepoLink is not None:
        sbItem = sb.get_item(item['id'])
        thisFileName = item['id'] + '_SourceCatalog.json'

        currentFiles = sb.get_item_file_info(sbItem)
        currentCatalogFile = next((f for f in currentFiles if f['name'] == thisFileName), None)

        if currentCatalogFile is not None:
            print('File Exists:', item['link']['url'])
        else:
            nhdRepoCatalog = nhd.build_nhd_repo_directory_listing(item['link']['url'], nhdRepoLink)
            thisFileName = item['id']+'_SourceCatalog.json'
            with open(thisFileName, 'w') as outfile:
                json.dump(nhdRepoCatalog, outfile)

            sb.upload_file_to_item(sbItem, thisFileName)
            os.remove(thisFileName)

            print('File Cached:', nhdRepoCatalog['Source ScienceBase Item'])
