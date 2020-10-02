'''
Created on 15 Nov 2019

@author: AVee
'''
import mwclient
from items import item
import io
import json

def run():
    site = mwclient.Site('chatwars-wiki.de', path='/')
    items = item.load_all_items(site)
    item.save_to_file('../data/resources_v2.json', items)
    item.save_to_file_v1('../data/resources.json', items)

if __name__ == '__main__':
    run()