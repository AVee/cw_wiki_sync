'''
Created on 15 Nov 2019

@author: AVee
'''
import mwclient
from items import item
from items.item import Item
import io

def run():
    site = mwclient.Site('chatwars-wiki.de', path='/')

    changes = site.recentchanges(namespace='0') # 0 being the magic number for the Main namespace
    # Refresh existing items
    items = item.load_from_file('../data/resources.json')
    try:
        with io.open('../data/lastrev') as f:
            maxrev = int(f.read())
    except Exception:
        maxrev = max(i.revision for i in items['items'])
    
    pages = None # Lazy loaded later only when needed
    lastrev = None
    
    # Run through changed pages
    for change in changes:
        if not change['revid'] > maxrev:
            break
        if not lastrev:
            lastrev = change['revid']
        
        page = next((i for i in items['items'] if i.pagename == change['title']), None)
        
        if page: # We had this item already, update.
            if page.revision < change['revid']:
                page.load(site)
                if not page._has_item: # No longer an item page (could be a page move/rename).
                    items.remove()
        else:
            if not pages: # Lazy load list of item pages
                pages = list(site.ask('[[ItemID::+]]'))
            
            if any(p for p in pages if p['fulltext'] == change['title']):
                itm = Item(change['title'])
                itm.load(site)
                
                if not itm._has_item:
                    continue
                 
                items['items'].append(itm)

    # Only save if there are changes
    if any(i for i in items['items'] if i.revision > maxrev):
        item.save_to_file('../data/resources.json', items)

    if lastrev:
        try:
            with io.open('../data/lastrev', 'w') as f:
                f.write(str(lastrev))
        except Exception as e:
            print(f'Failed to save lastrev: {e}')
        
    
if __name__ == '__main__':
    run()