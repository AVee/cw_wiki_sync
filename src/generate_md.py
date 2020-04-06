'''
Created on 6 Apr 2020

@author: AVee
'''
from items import item
import io

def write_links(f, items, extra = None):
    if items:
        for i in items:
            f.write(i.markdown_link() + '  \n')
            if extra:
                f.write(extra(i))
    else:
        f.write("Nothing found, that's looking good!  \n")
    
def run():
    items = item.load_from_file('../data/resources.json')
    allitems = items['items'] + items['incomplete']
    
    with io.open('../docs/missingid.md', 'w') as f:
        f.write('## Items with missing IDs\n\n')
        write_links(f, items['incomplete'])
        
    with io.open('../docs/wikinotes.md', 'w') as f:
        f.write('## Items with notes\n\n')
        write_links(f, [i for i in allitems if i.note.value], lambda i : f'_{i.note}_  \n\n')
                
    with io.open('../docs/recipestatus.md', 'w') as f:
        f.write('## Craftable items without recipe\n\n')
        write_links(f, [i for i in allitems if i.BoolCraft == True and not i.recipe])

        f.write('## Items with recipe marked incomplete\n\n')
        write_links(f, [i for i in allitems if i.BoolRecipeIncomplete.value == True])

        f.write('## Items with RecipeIncomplete unset\n\n')
        write_links(f, [i for i in allitems if i.BoolRecipeIncomplete.value == None])
        
if __name__ == '__main__':
    run()