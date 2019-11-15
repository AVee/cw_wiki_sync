'''
Created on 15 Nov 2019

@author: AVee
'''
import mwclient
from items import item
import io
import json
import items

def run():
    f = io.open('../data/resources.json', 'w')
    site = mwclient.Site('chatwars-wiki.de', path='/')
    items = item.load_all_items(site)
    json.dump(items, f, default=item.item_serialize, indent=4)
    f.close()

if __name__ == '__main__':
    run()