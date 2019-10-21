'''
Created on 21 Oct 2019

@author: AVee
'''
import mwparserfromhell
from time import sleep
import io
import mwclient
import glob
from pathlib import Path

def save_resource_pages():
    site = mwclient.Site('chatwars-wiki.de', path='/')
    pages = site.ask('[[ItemID::+]]')
    
    
    sleep(1)
     
    for page in pages:
        page2 = site.pages[page['fulltext']]
        text = page2.text()
        if text:
            print('Saving ' + page['fulltext'])
            f = io.open('../data/pages/' + page['fulltext'] + ".wiki", 'w+')
            f.write(text)
            f.close()
        else:
            print("!! No text for " + page['fulltext'])
    
        sleep(1)

def parse_resource_pages():
    result = {'items': {}, 'codes': {}}
    for file in glob.glob('../data/pages/*.wiki'):
        f = io.open(file)
        text = f.read()
        f.close()
        
        w = mwparserfromhell.parse(text)
        
        p = Path(file)
        itemName = p.stem
        item = { 'Name': itemName }
        recipe = {}
        for template in w.filter_templates():
            if str(template.name).strip() == 'Item' or str(template.name).strip() == '#set:':
                for param in template.params:
                    name = str(param.name).strip()
                    value = str(param.value).strip().split('\n', 1)[0] # More sanitizing may be needed
                    if value and not value.startswith('<!--'):
                        if value.lower() == 'false' or value.lower() == 'no':
                            value = False
                        elif value.lower() == 'true' or value.lower() == 'yes':
                            value = True
                        item[name] = value 
            elif str(template.name).strip() == '#subobject:':
                ingredient = False
                qty = False
                for param in template.params:
                    name = str(param.name).strip()
                    value = str(param.value).strip().split('\n', 1)[0] # More sanitizing may be needed
                    if name == 'Crafting ingredient' and value:
                        ingredient = value
                    if name == 'Qty' and value:
                        qty = value
                if ingredient and qty:
                    recipe[ingredient] = qty
                    item['recipe'] = recipe
        result['items'][itemName] = item
        try:
            result['codes'][item['ItemID']] = itemName
        except KeyError:
            print(f"No code for {itemName}")
            
    return result
        
        
parse_resource_pages()