'''
Created on 6 Apr 2020

@author: AVee
'''
from items import item
import io
from mwclient.client import Site
import secrets

def write_links(f, items, extra = None):
    if items:
        for i in items:
            f.write(f'[[{i.pagename}]]\n')
            if extra:
                f.write(extra(i))
            f.write('\n')
    else:
        f.write("Nothing found, that's looking good!  \n")
    
def run():
    items = item.load_from_file('../data/resources.json')
    allitems = items['items'] + items['incomplete']
    allitems.sort(key = lambda i : i.pagename)
    
    site = Site('chatwars-wiki.de', path='/')
    site.login(secrets.wiki_username, secrets.wiki_password)
    
    page = site.pages['Items needing attention']
    oldtext = page.text()
    
    f = io.StringIO()
    f.write('=Items needing attention=\n')
    f.write('This is an automatically generated page which list item pages where issues where detected. You can use this page to find things that might need to be fixed.\n\n')
    f.write("'''Please note:''' These checks run every hour, if you fixed something it might take a while before it shows here. Also, there is no point in editing this page, it will be overwritten automatically.\n\n")
    
    f.write('== Items with missing IDs ==\n')
    write_links(f, items['incomplete'])
        
    f.write('== Items with notes ==\n')
    write_links(f, [i for i in allitems if i.note.value], lambda i : f"''{i.note}''\n")
                
    f.write('== Craftable items without recipe ==\n')
    write_links(f, [i for i in allitems if i.BoolCraft.value == True and not i.recipe])

    f.write('== Items with recipe marked incomplete ==\n')
    write_links(f, [i for i in allitems if i.BoolRecipeIncomplete.value == True])

    f.write('== Items with RecipeIncomplete unset ==\n')
    write_links(f, [i for i in allitems if i.BoolCraft.value == True and i.BoolRecipeIncomplete.value == None])
    
    newtext = f.getvalue().strip()
    f.close()
    
    if oldtext != newtext:
        page.save(newtext, 'Automatic item checks')

if __name__ == '__main__':
    run()