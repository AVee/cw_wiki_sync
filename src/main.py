'''
Created on 21 Oct 2019

@author: Arjan
'''
import wiki_to_json
import json
import io

def run():
    #wiki_to_json.save_resource_pages()
    resources = wiki_to_json.parse_resource_pages()
    content = json.dumps(resources, indent = 1)
    f = io.open('../data/resources.json', 'w+')
    f.write(content)
    f.close()

if __name__ == '__main__':
    run()
