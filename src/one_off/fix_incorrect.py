'''
Created on 6 Apr 2020

@author: AVee
'''
from items import item
import io
from mwclient.client import Site
import secrets

def run():
    items = item.load_from_file('../../data/resources.json')
    allitems = items['items'] + items['incomplete']
    allitems.sort(key = lambda i : i.pagename)
    
    site = Site('chatwars-wiki.de', path='/')
    site.login(secrets.wiki_username, secrets.wiki_password)
    
    # Recipes/Parts can *always* be sold at Auction
#     tofix = [i for i in allitems if (i.ItemType.value == 'Recipe (Item)' or i.ItemType.value == 'Piece of Equipment') and i.BoolAuction.value != True]
#     print([i.pagename for i in tofix])
#     for page in tofix:
#         page.BoolAuction.value = True

    # Recipes/Parts can *never* be sold at Exchange
#     tofix = [i for i in allitems if (i.ItemType.value == 'Recipe (Item)' or i.ItemType.value == 'Piece of Equipment') and i.BoolExchange.value != False]
#     print([i.pagename for i in tofix])
#     for page in tofix:
#         page.BoolExchange.value = False

    # Recipes/Parts can't be wrapped
#     tofix = [i for i in allitems if i.Wrapping.value == 0]
#     print([i.pagename for i in tofix])
#     for page in tofix:
#         page.Wrapping.value = None
        
#     tofix = [i for i in allitems if (i.ItemType.value == 'Recipe (Item)' or i.ItemType.value == 'Piece of Equipment') and i.Weight.value != 10]
#     print([i.pagename for i in tofix])
#    for page in tofix:
#        page.Weight.value = 10
        
    # Recipes/Parts can *never* be sold at Exchange
#     tofix = [i for i in allitems if (i.ItemType.value == 'Recipe (Item)' or i.ItemType.value == 'Piece of Equipment') and i.BoolCraft.value != False]
#     print([i.pagename for i in tofix])
#     for page in tofix:
#         page.BoolCraft.value = False

    # Recipes/Parts never have a subtype
#     tofix = [i for i in allitems if (i.ItemType.value == 'Recipe (Item)' or i.ItemType.value == 'Piece of Equipment') and i.ItemSubType.value]
#     print([i.pagename for i in tofix])
#     for page in tofix:
#         page.ItemSubType.value = None

    # Recipes/Parts are always depositable
#     tofix = [i for i in allitems if (i.ItemType.value == 'Recipe (Item)' or i.ItemType.value == 'Piece of Equipment') and i.BoolDepositGuild.value != True]
#     print([i.pagename for i in tofix])
#     for page in tofix:
#         page.BoolDepositGuild.value = True




#     for page in allitems:
#         if page.dirty:
#             print(f'Saving {page.pagename}')
#             page.save(site, 'Fixing thing that can never be true (Round 4)')
            
if __name__ == '__main__':
    run()