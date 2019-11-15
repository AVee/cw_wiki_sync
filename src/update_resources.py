'''
Created on 15 Nov 2019

@author: AVee
'''
import io
import mwclient
from items import item
import json

def run():
    site = mwclient.Site('chatwars-wiki.de', path='/')

    f = io.open('../data/resources.json')
    items = json.load(f, object_hook=item.item_deserialize)
    f.close()
    for itm in items:
        itm.load(site)
    
    f = io.open('../data/resources.json', 'w')
    json.dump(items, f, default=item.item_serialize, indent=4)
    f.close()

if __name__ == '__main__':
    run()