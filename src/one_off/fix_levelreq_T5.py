'''
Created on 6 Apr 2020

@author: AVee
'''
from items import item
from mwclient.client import Site
import secrets

def run():
    items = item.load_from_file('../../data/resources.json')
    allitems = items['items'] + items['incomplete']
    allitems.sort(key = lambda i : i.pagename)
    
#     site = Site('chatwars-wiki.de', path='/')
#     site.login(secrets.wiki_username, secrets.wiki_password)
    
    print([i.pagename for i in allitems if i.LevelEquipRequirement.value == 55])
    
#     tofix = [i for i in allitems if i.LevelEquipRequirement.value == 55]
#     
#     for page in tofix:
#         page.LevelEquipRequirement.value = 60
#         page.save(site, 'Level equip requirement set to 60.')
    
if __name__ == '__main__':
    run()