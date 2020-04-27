'''
Created on 27 Apr 2020

@author: AVee
'''
from functools import lru_cache, wraps
from items import item
from mwclient.client import Site
from _collections_abc import Iterable
import mwparserfromhell

testmode = True

@lru_cache(1)    
def _load_items():
    return item.load_from_file()
    
@lru_cache(1)    
def _load_site():
    global testmode
    
    site = Site('chatwars-wiki.de', path='/')
    try:
        import secrets
        if not secrets.testmode:
            site.login(secrets.wiki_username, secrets.wiki_password)
            testmode = False
    except ImportError:
        pass
        
    return site

def pagegenerator(pages, comment):
    if not isinstance(pages, Iterable):
        pages = [pages]

    def decorator(func):
        @wraps(func)
        def _function_wrapper():
            items = _load_items()
            site = _load_site()

            # Check pages first.            
            sitePages = []
            for page in pages:
                sitePage = site.pages[page]
                if not sitePage.exists:
                    if testmode:
                        print(f"WARNING: Page {page} does not exist!")
                    else:
                        raise Exception(f"Page {page} does not exist, refusing to add new page.")
                sitePages.append(sitePage)
                    
            results = func(items)
            
            if not isinstance(results, Iterable):
                results = [results]
            
            if len(pages) != len(results):
                raise Exception(f"Expected {len(pages)} results but got {len(results)} instead.")
            
            for i in range(0, len(pages)):
                if not results[i] or len(results[i]) < 100:
                    raise Exception(f'Resulting page is less then 100 character, seems like something when wrong.')
                
                # Add warning about aut-generated pages
                results[i] = '<!--\nWARNING: DO NOT CHANGE!\nThis section is automatically generated, any changes you make will be overwritten. Also leave the above <div> intact.\nIf you spot an error here ping @AVee00 in the @cwwikiTaskforce group.\n(Any content outside of this div can be edited and will be preserved.)\n-->\n' + results[i]
                text = sitePages[i].text()
                parsed = mwparserfromhell.parse(text)
                tags = parsed.filter_tags(matches=tagfilter)
                
                if len(tags) == 0:
                    raise Exception(f'No section (div) for generated content found.')
                elif len(tags) > 1:
                    raise Exception(f'Multiple sections (div) for generated content found.')
                
                tag = tags[0]
                oldtext = str(tag.contents)
                
                if testmode:
                    print(f'****** Result for {pages[i]} {"(changed)" if results[i] != oldtext else "(unchanged)"} ******')
                    print(results[i] + '\n')
                elif results[i] != oldtext:
                    tag.contents = results[i]
                    sitePages[i].save(str(parsed), comment)
                    
        return _function_wrapper
    
    return decorator

def tagfilter(node: mwparserfromhell.nodes.Node):
    return isinstance(node, mwparserfromhell.nodes.tag.Tag) and node.tag == 'div' and any([a for a in node.attributes if a.name == 'id' and a.value == 'wikibot_generated_content'])