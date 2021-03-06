'''
Created on 10 Nov 2019

@author: AVee
'''
from items.properties import Property, BoolProperty, IntProperty, LinkProperty,\
    SetProperty, SetListProperty
from mwclient.client import Site
import mwparserfromhell
import mwclient
import json
from mwparserfromhell.nodes.template import Template
from mwparserfromhell.nodes.text import Text
from mwparserfromhell.nodes.extras.parameter import Parameter
from mwclient.page import Page
from mwclient import page
import io
from typing import List, Union
from datetime import datetime, timezone
import urllib
from importlib.resources import path
import os
from distutils.util import strtobool

class Item(object):
    def __init__(self, pagename:str=None, page:Page=None, **kwargs):
        super().__init__(**kwargs)
        
        self.ItemID = Property(json_name='id')
        self.BoolEventItem = BoolProperty(json_name='eventItem')
        self.Event = LinkProperty(json_name='eventPage')
        self.InGameName = Property(json_name='name')
        self.ItemType = SetProperty(json_name='type')
        self.ItemSubType = SetProperty(json_name='subType')
        self.ArmorClass = SetProperty(json_name='armorClass')
        self.DetailedDescription = Property(json_name='description')
        self.note = Property(json_name='wikiNote')
        self.Attack = IntProperty(json_name='attack')
        self.Defense = IntProperty(json_name='defense')
        self.Mana = IntProperty(json_name='mana')
        self.Stamina = IntProperty(json_name='stamina')
        self.InventoryIncrease = IntProperty(json_name='inventoryIncrease')
        self.Luck = IntProperty(json_name='luck')
        self.BaseDuration = IntProperty(json_name='duration')
        self.PotionEffect = Property(json_name='effect')
        self.Weight = IntProperty(json_name='weight')
        self.Wrapping = IntProperty(json_name='wrapping')
        self.LevelEquipRequirement = IntProperty(json_name='levelRequirement')
        self.Ammunition = SetListProperty(json_name='ammunition')
        self.BoolDepositGuild = BoolProperty(json_name='depositable')
        self.ShopBuyPrice = IntProperty(json_name='shopBuyPrice')
        self.ShopSellPrice = IntProperty(json_name='shopSellPrice')
        self.BoolExchange = BoolProperty(json_name='exchange')
        self.BoolAuction = BoolProperty(json_name='auction')
        self.FreeTextOverview = Property(json_name='freeText')
        self.BoolQuest = BoolProperty(json_name='quest')
        self.PlayerQuestMinLevel = IntProperty(json_name='questMinLevel')
        self.PerceptionLevel = IntProperty(json_name='questPerceptionLevel')
        self.QuestForestMorning = BoolProperty(json_name='dropForestMorning')
        self.QuestForestDay = BoolProperty(json_name='dropForestDay')
        self.QuestForestEvening = BoolProperty(json_name='dropForestEvening')
        self.QuestForestNight = BoolProperty(json_name='dropForestNight')
        self.QuestSwampMorning = BoolProperty(json_name='dropSwampMorning')
        self.QuestSwampDay = BoolProperty(json_name='dropSwampDay')
        self.QuestSwampEvening = BoolProperty(json_name='dropSwampEvening')
        self.QuestSwampNight = BoolProperty(json_name='dropSwampNight')
        self.QuestValleyMorning = BoolProperty(json_name='dropValleyMorning')
        self.QuestValleyDay = BoolProperty(json_name='dropValleyDay')
        self.QuestValleyEvening = BoolProperty(json_name='dropValleyEvening')
        self.QuestValleyNight = BoolProperty(json_name='dropValleyNight')
        self.QuestForayMorning = BoolProperty(json_name='dropForayMorning')
        self.QuestForayDay = BoolProperty(json_name='dropForayDay')
        self.QuestForayEvening = BoolProperty(json_name='dropForayEvening')
        self.QuestForayNight = BoolProperty(json_name='dropForayNight')
        self.BoolEnchantment = BoolProperty(json_name='enchantable')
        self.EnchantAtk1 = IntProperty(json_name='enchantAtk1')
        self.EnchantAtk2 = IntProperty(json_name='enchantAtk2')
        self.EnchantAtk3 = IntProperty(json_name='enchantAtk3')
        self.EnchantAtk4 = IntProperty(json_name='enchantAtk4')
        self.EnchantDef1 = IntProperty(json_name='enchantDef1')
        self.EnchantDef2 = IntProperty(json_name='enchantDef2')
        self.EnchantDef3 = IntProperty(json_name='enchantDef3')
        self.EnchantDef4 = IntProperty(json_name='enchantDef4')
        self.EnchantMana1 = IntProperty(json_name='enchantMana1')
        self.EnchantMana2 = IntProperty(json_name='enchantMana2')
        self.EnchantMana3 = IntProperty(json_name='enchantMana3')
        self.EnchantMana4 = IntProperty(json_name='enchantMana4')
        self.BoolCraft = BoolProperty(json_name='craftable')
        self.BoolRecipeIncomplete = BoolProperty(json_name='recipeIncomplete')
        self.CraftCommand = Property(json_name='craftCommand')
        self.SkillCraft = SetProperty(json_name='craftSkill')
        self.SkillCraftLevel = IntProperty(json_name='craftLevel')
        self.ManaCrafting = IntProperty(json_name='craftMana')
        self.FreeText = Property(json_name='wikiFreeText')

        self.recipe = []
        
        self.pagename = pagename
        self._page = page

        self.lastModified = None
        self.revision = None
        self.wikiUrl = None
        
        if self._page:
            self._apply_page(self._page)
        
        self._dirty = False
        self._has_item = False

    def _apply_page(self, page:Page):
        self.pagename = page.page_title
        self.revision = page.revision
        self.lastModified = page._info.get('touched')
        self.wikiUrl = 'https://chatwars-wiki.de/index.php?title=' + urllib.parse.quote_plus(self.pagename)

    def save(self, site: Site, summary: str, allow_new = False):
        self._page = site.pages[self.pagename]
        if not self._page.exists and not allow_new:
            raise Exception('Refusing to create new pages.')
        if not self._has_item:
            raise Exception("Invalid item state, page doesn't seem to contain an Item")
        self._page.save(self.wiki_text(), summary)
        self._apply_page(self._page)
        self.dirty = False
        
    def load(self, site: Site, page: Page=None):
        if page:
            self._page = page
        else:
            self._page = site.pages[self.pagename]
        if self.dirty or not self.revision or self.revision != self._page.revision:
            text = self._page.text()
            self.parse(text)
            self._apply_page(self._page)
    
    def clear(self):
        for v in self.__dict__.values():
            if isinstance(v, Property) and v.value != None:
                v.value = None
        self._dirty = False
        self._has_item = False
        self.recipe = []
        self.lastModified = None
        self.revision = None
        self.wikiUrl = None
    
    def parse(self, text):
        self.clear()
        w = mwparserfromhell.parse(text)
        item_found = False
        for template in w.filter_templates():
            if str(template.name).strip() == 'Item':
                item_found = True
                for param in template.params:
                    name = str(param.name).strip()
                    value = str(param.value).strip() # More sanitizing may be needed
                    if value and not value.startswith('<!--'):
                        try:
                            getattr(self, name).value = value
                        except Exception as e:
                            print(str(e))
                w.nodes.remove(template)
            elif str(template.name).strip() == '#subobject:':
                # There may be empty items
                if not template.params:
                    w.nodes.remove(template)
                    continue
                
                ingredient = {}
                for param in template.params:
                    name = str(param.name).strip()
                    value = str(param.value).strip().split('\n', 1)[0] # More sanitizing may be needed
                    if name == 'Crafting ingredient' and value:
                        ingredient['name'] = value
                    if name == 'Qty' and value:
                        ingredient['qty'] = value
                    if name == 'Personalized' and value:
                        ingredient['personalized'] = strtobool(str(value)) != 0
                    if name == 'PersonalizedSetNr' and value:
                        ingredient['personalizedSetNr'] = value
                if 'name' in ingredient and 'qty' in ingredient:
                    if not 'personalized' in ingredient:
                        ingredient['personalized'] = False
                        
                    self.recipe.append(ingredient);
                    w.nodes.remove(template)
        
        free = str(w).strip()
        if free != '':            
            self.FreeText.value = free
            
        self.dirty = False
        self._has_item = item_found
    
    def wiki_text(self):
        w = mwparserfromhell.parse("{{Item}}\n")
        item = w.filter_templates()[0]

        for k,v in self.__dict__.items():
            if isinstance(v, Property) and v.get_wiki_value() != None and k != 'FreeText':
                item.add(k, v.get_wiki_value()) 
        
        for ingredient in self.recipe:
            sub = Template('#subobject:', params=[Parameter('Crafting ingredient',ingredient['name']), Parameter('Qty', ingredient['qty'])])
            sub.add('Personalized', ('Yes' if ingredient['personalized'] else 'No'))
            if 'personalizedSetNr' in ingredient:
                sub.add('PersonalizedSetNr', ingredient['personalizedSetNr'])
            w.nodes.append(sub)
            w.nodes.append(Text('\n'))
        
        result = str(w)
        if self.FreeText.get_wiki_value() != None:
            result = result + '\n' + self.FreeText.get_wiki_value()
        
        return result
    
    def markdown_link(self):
        return f"[{self.pagename}]({self.wikiUrl})"
    
    @property
    def dirty(self):
        if self._dirty:
            return True
        
        for key in dir(self):
            try:
                if key != 'dirty' and getattr(self, key)._dirty:
                    return True
            except AttributeError:
                pass
        
        return False
    
    @dirty.setter
    def dirty(self, value):
        self._dirty = value
        
        if not value:
            for key in dir(self):
                try:
                    if key != 'dirty':
                        getattr(self, key)._dirty = value
                except AttributeError:
                    pass

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.__dict__ == other.__dict__
        return NotImplemented

def item_by_id(site: Site, item_id: str):
    pages = site.ask(f'[[ItemID::{item_id}]]')
    page = next(pages)
    # We should have an unique result
    try:
        next(pages)
        raise Exception(f"Item with id '{item_id}' not unique.")
    except StopIteration:
        pass
    item = Item(pagename=page['fulltext'])
    item.load(site)
    return item

def item_by_pagename(site: Site, pagename: str):    
    item = Item(pagename=pagename)
    item.load(site)
    return item

def item_by_ingamename(site: Site, name: str):
    pages = site.ask(f'[[InGameName::{name}]]')
    page = next(pages)
    # We should have an unique result
    try:
        next(pages)
        raise Exception(f"Item with in-game name '{name}' not unique.")
    except StopIteration:
        pass
    item = Item(pagename=page['fulltext'])
    item.load(site)
    return item
    
def load_all_items(site: Site):
    pages = site.ask('[[ItemID::+]]')

    items = []
    for page in pages:
        item = Item(pagename=page['fulltext'])
        item.load(site)
        items.append(item)
        
    return items

def load_from_file(path: str = None):
    if not path:
        path = os.path.join(os.path.dirname(__file__), '../../data/resources_v2.json')
        
    with io.open(path, encoding='utf-8') as f:
        items = json.load(f, object_hook=item_deserialize)
        if items['format'] != 2:
            raise Exception('Wrong format (should be 2).')
        return items

def save_to_file(path: str, items: Union[List[Item], dict]):
    if isinstance(items, dict):
        items = items['items'] + items['incomplete']
    
    result = { 'timestamp': datetime.now(tz=timezone.utc).isoformat(), 'deprecated': False, 'obsolete': False, 'format': 2, 'items': [i for i in items if i._has_item and i.ItemID.value != '' and i.ItemID.value != '??'], 'incomplete': [i for i in items if i._has_item and (i.ItemID.value == '' or i.ItemID.value == '??')] }
    
    with io.open(path, 'w', encoding='utf-8') as f:
        json.dump(result, f, default=item_serialize, indent=4, ensure_ascii=False)

def save_to_file_v1(path: str, items: Union[List[Item], dict]):
    if isinstance(items, dict):
        items = items['items'] + items['incomplete']
    
    result = { 'timestamp': datetime.now(tz=timezone.utc).isoformat(), 'deprecated': True, 'obsolete': False, 'format': 1, 'items': [i for i in items if i._has_item and i.ItemID.value != '' and i.ItemID.value != '??'], 'incomplete': [i for i in items if i._has_item and (i.ItemID.value == '' or i.ItemID.value == '??')] }
    
    with io.open(path, 'w', encoding='utf-8') as f:
        json.dump(result, f, default=item_serialize_v1, indent=4, ensure_ascii=False)

def item_serialize(obj):
    if isinstance(obj, Item):
        result = { v.json_name:v.value for v in obj.__dict__.values() if isinstance(v, Property) and v.value != None }
        result.update({ k:v for k,v in obj.__dict__.items() if not k.startswith("_") and not isinstance(v, Property) })
        return result

def item_serialize_v1(obj):
    if isinstance(obj, Item):
        result = { v.json_name:v.value for v in obj.__dict__.values() if isinstance(v, Property) and v.value != None }
        result.update({ k:v for k,v in obj.__dict__.items() if not k.startswith("_") and not isinstance(v, Property) })
        if obj.recipe:
            new_recipe = {}
            for ingredient in obj.recipe:
                new_recipe[ingredient['name']] = ingredient['qty']
            result['recipe'] = new_recipe    
        return result

def item_deserialize(dct):
    if 'pagename' in dct:
        item = Item(dct['pagename'])
        for k,v in item.__dict__.items():
            if isinstance(v, Property):
                try:
                    v.value = dct[v.json_name]
                except KeyError:
                    pass
            elif not k.startswith('_'):
                try:
                    setattr(item, k, dct[k])
                except KeyError:
                    pass
        item.dirty = False
        item._has_item = True
        return item
    
    return dct
