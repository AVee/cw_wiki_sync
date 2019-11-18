'''
Created on 14 Nov 2019

@author: AVee
'''
from tests import test_pages
from items.item import Item
import mwclient
import items

def test_parse_all():
    for p, t in test_pages.pages.items():
        item = Item(pagename=p)
        item.parse(t)
        
        new = item.wiki_text()
        new = "".join(new.split())
        old = "".join(test_pages.results[p].split())
        assert new == old, f"Mismatch in {p}"
        
def test_dirty():
    item = Item(pagename='Lion Boots')
    item.parse(test_pages.pages['Lion Boots'])
    
    assert not item.dirty

    # same value...    
    item.Attack.value = 6
    
    assert not item.dirty
    assert not item.Attack._dirty
    assert not item.BoolAuction._dirty

    # different value...    
    item.Attack.value = 20

    assert item.dirty
    assert item.Attack._dirty
    assert not item.BoolAuction._dirty

    item.dirty = True
    
    assert item.dirty
    assert item.Attack._dirty
    assert not item.BoolAuction._dirty
    
    item.dirty = False
        
    assert not item.dirty
    assert not item.Attack._dirty
    assert not item.BoolAuction._dirty

def test_file():
    itms = items.item.load_from_file('../data/resources.json')
    items.item.save_to_file('../data/resources.json.test', itms)
    itms2 = items.item.load_from_file('../data/resources.json.test')
    del(itms['timestamp'])
    del(itms2['timestamp'])
    assert itms == itms2
    
def test_loading():    
    item = Item(pagename='Lion Boots')
    site = mwclient.Site('chatwars-wiki.de', path='/')
    item.load(site)
    
    assert not item.dirty
    assert not item.Attack._dirty
    assert not item.BoolAuction._dirty
    assert item.BoolCraft.value
    assert item.ItemID.value == "a61"
    
    item.Attack.value = 25
    
    assert item.dirty
    assert item.Attack._dirty
    assert not item.BoolAuction._dirty

    # refresh
    item.load(site)

    assert not item.dirty
    assert not item.Attack._dirty
    assert not item.BoolAuction._dirty
    assert item.BoolCraft.value
    assert item.ItemID.value == "a61"
    