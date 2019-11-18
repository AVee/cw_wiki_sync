'''
Created on 18 Nov 2019

@author: AVee
'''
from items import item
import io
import json
from mwclient.client import Site
import secrets

site = Site('chatwars-wiki.de', path='/')
site.login(secrets.wiki_username, secrets.wiki_password)

def single(list):
    if len(list) > 1:
        raise IndexError('Multiple items found.')
    return list[0]

def jj_missing_items():
    items = item.load_from_file('../../data/resources.json')['items']
    
    with io.open('jj_dump.json', encoding='utf-8') as f:
        resources = json.load(f)
    
    for v in items:
        try:
            if v.InGameName.value != None:
                row = single([i for i in resources['values'] if v.InGameName.value == i[1]])
                if row[0] != v.ItemID.value:
                    print(f"Id mismatch {row[0]} / {v.ItemID.value} {v.pagename}")
        except IndexError as e:
            try:
                row = single([i for i in resources['values'] if v.InGameName.value.lower() == i[1].lower()])
                print(f"Case mismatch {v.InGameName.value} / {row[1]} {v.pagename}")
                if row[0] != v.ItemID.value:
                    print(f"Id mismatch {row[0]} / {v.ItemID.value} {v.pagename}")
            except IndexError as e:
                pass #print(f'Item name {v.InGameName.value} not found. {v.pagename}')
        try:
            row = single([i for i in resources['values'] if v.ItemID.value == i[0]])
            if v.InGameName.value != None:
                if row[1].lower() != v.InGameName.value.lower():
                    print(f"Name mismatch {row[1]} / {v.InGameName.value} {v.pagename}")
                elif row[1] != v.InGameName.value:
                    print(f"Case mismatch {row[1]} / {v.InGameName.value} {v.pagename}")
            else:
                print(f"Found in game name {row[1]} / {row[0]} {v.pagename}")
        except IndexError as e:
            pass #print(f'Item {v.ItemID.value} not found. {v.pagename}')

def fix_ingame_case():    
    items = item.load_from_file('../../data/resources.json')['items']
    
    with io.open('jj_dump.json', encoding='utf-8') as f:
        resources = json.load(f)
    
    for v in items:
        try:
            if v.InGameName.value != None:
                row = single([i for i in resources['values'] if v.ItemID.value == i[0]])
                if row[1] != v.InGameName.value and row[1].lower() == v.InGameName.value.lower():
                    v.load(site) # Refresh
                    v.InGameName.value = row[1]
                    if v.dirty:
                        v.save(site, 'Fix casing on in-game name')
        except IndexError as e:
            print(f'Item {v.ItemID.value} not found. {v.pagename}')
    
def jj_new_items():        
    items = item.load_from_file('../../data/resources.json')['items']
    
    with io.open('jj_dump.json', encoding='utf-8') as f:
        resources = json.load(f)

    for row in resources['values']:
        try:
            itm = row = single([v for v in items if v.ItemID.value == row[0]])
        except IndexError as e:
            print(f'New item {row[1]} {row[0]}')
        
def run():
    jj_missing_items()
    #fix_ingame_case()
    jj_new_items()
    
#     page = site.pages['Loyalty Trophy']
#     page.save('{{Item|ItemID=tlt|InGameName=Loyalty Trophy|BoolEventItem=No|ItemType=Misc|BoolDepositGuild=Yes|BoolExchange=No|BoolAuction=No|BoolQuest=No|BoolEnchantment=No|BoolCraft=No}}', 'Add missing items')
    
if __name__ == '__main__':
    run()