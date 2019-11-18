'''
Created on 15 Nov 2019

@author: AVee
'''
import mwclient
from items import item
from items.item import Item

def run():
    site = mwclient.Site('chatwars-wiki.de', path='/')

    # Refresh existing items
    items = item.load_from_file('../data/resources.json')
    for itm in items['items']:
        itm.load(site)
    
    # Find new items
    pages = site.ask('[[ItemID::+]]')
    
    for page in pages:
        name = page['fulltext']
        if not any([i for i in items['items'] if i.pagename == name]):
            itm = Item(pagename=name)
            itm.load(site)
            items['items'].append(itm)

    item.save_to_file('../data/resources.json', items)
    
if __name__ == '__main__':
    run()