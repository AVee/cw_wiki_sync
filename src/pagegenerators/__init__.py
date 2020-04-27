from pagegenerators import items_needing_attention
from functools import wraps
from functools import lru_cache
from items import item

def run_all():
    items_needing_attention.run();

if __name__ == '__main__':
    run_all()