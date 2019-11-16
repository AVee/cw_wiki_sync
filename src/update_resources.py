'''
Created on 15 Nov 2019

@author: AVee
'''
import mwclient
from items import item

def run():
    site = mwclient.Site('chatwars-wiki.de', path='/')

    items = item.load_from_file('../data/resources.json')
    for itm in items:
        itm.load(site)
    
    item.save_to_file('../data/resources.json', items)
    
if __name__ == '__main__':
    run()