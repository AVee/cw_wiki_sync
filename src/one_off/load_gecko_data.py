'''
Created on 16 Nov 2019

@author: AVee
'''
from items import item
import csv
import io
from mwclient.client import Site
import secrets
import emoji
import re
from items.item import Item

site = Site('chatwars-wiki.de', path='/')
site.login(secrets.wiki_username, secrets.wiki_password)

def single(list):
    if len(list) > 1:
        raise IndexError('Multiple items found.')
    return list[0]

def item_type(type:str):
    if type in ['Dagger', 'Spear', 'Shield', 'Blunt', 'Bow', 'Sword']:
        return 'Weapon'
    elif type in ['Armor', 'Helmet', 'Shoes', 'Gloves', 'Boots']:
        return 'Protective Gear'
    elif type in ['Pet Coupon', 'Guild banner', 'Misc']:
        return 'Misc'
    elif type in ['Special Equippable', 'Ring', 'Amulet']:
        return 'Special Equippable'
    else:
        raise Exception('Unknown type')
    
def create_new_page(row):
    name = row['itemname']

    
    if 'croll' in name:
        print(f'Skipping {name}')
        return 
    if 'Coupon' in name:
        return
    #clean_name = demojize(row['itemname'])
    if name.startswith(emoji.emojize(':man_zombie:')):
        name = re.sub(emoji.get_emoji_regexp(), "", name) + ' (Event Item)'
    elif name.startswith(emoji.emojize(':wolf_face:')):
        name = re.sub(emoji.get_emoji_regexp(), "", name) + ' (Wolf)'
    elif name.startswith(emoji.emojize(':eagle:')):
        name = re.sub(emoji.get_emoji_regexp(), "", name) + ' (Eagle)'
    elif name.startswith(emoji.emojize(':dragon:')):
        name = re.sub(emoji.get_emoji_regexp(), "", name) + ' (Dragon)'
    elif name.startswith(emoji.emojize(':admission_tickets:')):
        pet = re.search("[^ ]*$", name).group()
        pet = re.sub("'", "", pet)
        name = 'Gift Coupon: ' + pet
    name = name.strip()
    
    print(f"{row['itemname']}:\t\t|{name}|")
    
    itm = Item(pagename=name)
    itm.ItemID.value = row['id']
    type = row['type'] if row['type'] != 'Shoes' else 'Boots'
    itm.ItemType.value = item_type(type)
    type = type if itm.ItemType.value not in ['Misc', 'Special Equippable'] else None
    itm.ItemSubType.value = type
    itm.InGameName.value = row['itemname']
    itm.BoolEventItem.value = ('Event' in name)
    if 'Coupon' in name:
        pet = re.search("[^ ]*$", name).group()
        itm.FreeTextOverview.value = f"The [[Gift Coupon]] can be traded for a [[{pet}]] at the :Paws: [[Menagerie]] in the [[Shop|castle shop]]."
        itm.BoolCraft.value = False
        itm.BoolAuction.value = True
        itm.BoolDepositGuild.value = True
        itm.BoolEnchantment.value = False
        itm.BoolExchange.value = False
        itm.BoolQuest.value = False
        
    if row['Attack']:
        itm.Attack.value = row['Attack']
    if row['Defense']:
        itm.Defense.value = row['Defense']
    if row['Mana']:
        itm.Mana.value = row['Mana']
    if row['Tier'] == '0':
        itm.LevelEquipRequirement.value = 0
    elif row['Tier'] == '1':
        itm.LevelEquipRequirement.value = 15
    elif row['Tier'] == '2':
        itm.LevelEquipRequirement.value = 25
    elif row['Tier'] == '3':
        itm.LevelEquipRequirement.value = 35
    elif row['Tier'] == '4':
        itm.LevelEquipRequirement.value = 45
    
    if row['Forest_Morning'] == '0' and \
            row['Forest_Day'] == '0' and \
            row['Forest_Evening'] == '0' and \
            row['Forest_Night'] == '0' and \
            row['Swamp_Morning'] == '0' and \
            row['Swamp_Day'] == '0' and \
            row['Swamp_Evening'] == '0' and \
            row['Swamp_Night'] == '0' and \
            row['Valley_Morning'] == '0' and \
            row['Valley_Day'] == '0' and \
            row['Valley_Evening'] == '0' and \
            row['Valley_Night'] == '0' and \
            row['Foray_Morning'] == '0' and \
            row['Foray_Day'] == '0' and \
            row['Foray_Evening'] == '0' and \
            row['Foray_Night'] == '0':
        itm.BoolQuest.value = False
    else:
        raise Exception("Didn't expect drop data.")
    
    print(itm.wiki_text())
    print('Created: https://chatwars-wiki.de/index.php?title=' + name)
    itm.save(site, "New items from GrumpyGecko", allow_new=True)

def create_new():
    items = item.load_from_file('../../data/resources.json')
    
    with io.open('gecko_items.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            try:
                itm = single([i for i in items if i.ItemID.value == row['id']])
                #print(f'Found {itm.pagename}')
            except IndexError as e:
                if str(e) == 'list index out of range':
                    create_new_page(row)
                else:
                    print(f"{row['itemname']}: {e}")

def fill_ingame_names():
    items = item.load_from_file('../../data/resources.json')
    
    with io.open('gecko_items.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            try:
                itm = single([i for i in items if i.ItemID.value == row['id']])
                
                if row['itemname'] and itm.InGameName.value != row['itemname']:
                    itm.load(site) # Refresh
                    if itm.InGameName.value == None:
                        itm.InGameName.value = row['itemname']
                        print(f'{itm.pagename}: {itm.InGameName.value}')
                        itm.save(site, "Setting in-game name")
                    elif row['itemname'] and itm.InGameName.value != row['itemname']:
                        print(f"Name mismatch: {itm.InGameName.value} on wiki vs {row['itemname']} in file.")

                    
                
            except IndexError as e:
                print(f'Item {row["id"]} not found.')
                
def run():
    #create_new()
    fill_ingame_names()
    
if __name__ == '__main__':
    run()