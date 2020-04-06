# Chatwars Wiki Items
This site contains a json file containing all known information of the items in Chatwars as found on the [chatwars wiki](https://chatwars-wiki.de/). Updates are run hourly and the latest file can be found in [resources.json](https://raw.githubusercontent.com/AVee/cw_wiki_sync/master/data/resources.json).

If any item data is missing or incomplete please just edit the wiki, it has a really nice form for editing item information ;-) Really, just go and improve what is on the wiki, the quality of this data depends on contributions to the wiki from users like you...

## Notes on resources.json
The intention is to keep the the file backwards compatible whenever possible. So new fields may be added, but existing fields will not be changed or removed. There are two top flags in the file indicating it's status, `deprecated` and `obsolete`. If the deprecated flag is set to true this indicates there is a newer format available and support for this version of the file will end at some point. If the obsolete becomes true the file is no longer automatically updated and the new version must be used to get the most recent data.

All known values for certain fields are included in the file, null values are not included. This means missing keys should generally be considered unknown (or not applicable).

There are two collections in the file, the first being 'items', which contains all valid items. The second is the 'incomplete' collection which contains all items for which the ID is missing. Separating these allows users of the json file to just work with the complete items and ignore work-in-progress items when new stuff is released in Chatwars.

## Issue lists
Apart from the json file a few lists are generated with items which might need attention:  

[Items without ID](missingid.md)  
[Items with notes](wikinotes.md)  
[Recipe status](recipestatus.md)  

