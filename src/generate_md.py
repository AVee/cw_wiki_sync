'''
Created on 6 Apr 2020

@author: AVee
'''
from items import item
import io
def run():
    items = item.load_from_file('../data/resources.json')

    with io.open('../doc/missingid.md', 'w') as f:
        f.write('## Items with missing IDs\n\n')
        
        for i in items['incomplete']:
            f.write(i.markdown_link() + '  \n')
        
    with io.open('../doc/wikinotes.md', 'w') as f:
        f.write('## Items with notes\n\n')
        
        for i in (items['items'] + items['incomplete']):
            if i.note.value:
                f.write(i.markdown_link() + '  \n')
                f.write(f'_{i.note}_  \n\n')
        
if __name__ == '__main__':
    run()