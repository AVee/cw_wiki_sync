'''
Created on 6 Apr 2020

@author: AVee
'''
from items import item
from dataclasses import field
from items.properties import Property
from mwclient.client import Site
import secrets
import io
from pagegenerators.tools import pagegenerator

errors = []

class ItemValueError:
    def __init__(self, field, message):
        self.field = field
        self.message = message

def must_have_value(i, field, message = 'Must have a value'):
    val = i.__dict__[field]
    if val == None or val == '':
        errors.append(ItemValueError(field, message))
    elif isinstance(val, Property) and (val.value == None or val.value == ''):
        errors.append(ItemValueError(field, message))

def must_be_empty(i, field, message = 'Must be empty'):
    val = i.__dict__[field]
    if not isinstance(val, Property) and val != None and val != '':
        errors.append(ItemValueError(field, message))
    elif isinstance(val, Property) and val.value != None and val.value != '':
        errors.append(ItemValueError(field, message))

def must_be_true(i, field, message = 'Must be True'):
    val = i.__dict__[field]
    if not isinstance(val, Property) and val != True:
        errors.append(ItemValueError(field, message))
    elif isinstance(val, Property) and val.value != True:
        errors.append(ItemValueError(field, message))

def must_be_false(i, field, message = 'Must be False'):
    val = i.__dict__[field]
    if not isinstance(val, Property) and val != False:
        errors.append(ItemValueError(field, message))
    elif isinstance(val, Property) and val.value != False:
        errors.append(ItemValueError(field, message))

def must_be_in(i, field, set):
    val = i.__dict__[field]
    if not val.value in set:
        errors.append(ItemValueError(field, f'value must be one of {str(list)}'))

@pagegenerator(['Items needing attention', 'Items needing attention (without notes)'], 'Automatic item checks')    
def run(items):
    global errors

    allitems = items['items'] + items['incomplete']
    allitems.sort(key = lambda i : i.pagename)

    f = io.StringIO()
    f2 = io.StringIO()
    
    for i in allitems:
        result = f"{i.pagename}:"
        errors = []
        must_have_value(i, 'ItemID')
        must_have_value(i, 'BoolEventItem')
        must_have_value(i, 'InGameName')
        must_have_value(i, 'ItemType')
        must_be_in(i, 'ItemType', {'Recipe (Item)', 'Weapon', 'Consumable', 'Misc', 'Piece of Equipment', 'Cape', 'Pet Food', 'Protective Gear', 'Resource', 'Special Equippable'})
        must_have_value(i, 'BoolDepositGuild')
        must_have_value(i, 'BoolExchange')
        must_have_value(i, 'BoolAuction')
        must_have_value(i, 'BoolQuest')
        must_have_value(i, 'BoolEnchantment')
        must_have_value(i, 'BoolCraft')
        
        if i.BoolEventItem.value:
            must_have_value(i, 'Event', 'Must be set on Event items')
            
        if i.ItemType.value == 'Recipe (Item)' or i.ItemType.value == 'Piece of Equipment':
            must_be_empty(i, 'ItemSubType', 'Must be empty on Recipes/Parts ***autofix***')
            must_have_value(i, 'Weight', 'Must be set on Recipes/Parts')
            must_have_value(i, 'LevelEquipRequirement', 'Must be set on Recipes/Parts')
            must_be_true(i, 'BoolDepositGuild', 'Recipes/Parts are always Depositable ***autofix***')
            must_be_true(i, 'BoolAuction', 'Recipes/Parts are always Auctionable ***autofix***')
            must_be_true(i, 'BoolQuest', 'Recipes/Parts are always Questable ***autofix***')
            must_be_false(i, 'BoolExchange', 'Recipes/Parts can never be traded at Exchange ***autofix***')
            must_be_empty(i, 'Wrapping', "Recipes/Parts can't be wrapped ***autofix***")
            must_be_empty(i, 'ShopBuyPrice', 'Recipes/Parts can never be traded at Shop ***autofix***')
            must_be_empty(i, 'ShopSellPrice', 'Recipes/Parts can never be traded at Shop ***autofix***')
            must_be_false(i, 'BoolCraft', 'Recipes/Parts can never be crafted ***autofix***')

        if i.ItemType.value == 'Weapon':
            must_have_value(i, 'ItemSubType', 'Must be set on Weapons')
            must_have_value(i, 'Weight', 'Must be set on Weapons')
            must_have_value(i, 'Wrapping', 'Must be set on Weapons')
        
        if i.BoolCraft.value:
            must_have_value(i, 'BoolRecipeIncomplete', 'Must be set on Craftable items')
            must_have_value(i, 'recipe', 'Craftable items must have a recipe')
        
        valid = not any(errors) and not i.note.value
        if not valid:
            f.write(f"'''[[{i.pagename}]]''' ([{i.wikiUrl}&action=formedit edit])\n")
            if i.note.value:
                f.write(f"* Note: ''{i.note.value}''\n")
            for e in errors:
                f.write(f"* {e.field}: {e.message}\n")
                
        if any(errors):
            f2.write(f"'''[[{i.pagename}]]''' ([{i.wikiUrl}&action=formedit edit])\n")
            for e in errors:
                f2.write(f"* {e.field}: {e.message}\n")
            

    newtext = f.getvalue().strip()
    f.close()
    
    newtext2 = f2.getvalue().strip()
    f2.close()
    
    return [newtext, newtext2]

if __name__ == '__main__':
    run()