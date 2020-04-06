# Chatwars Wiki Sync
This tool parses item data from [chatwars wiki](https://chatwars-wiki.de/) and produces a json file containing all known information of the items. 

The primary goal is to use the wiki as the *one source of truth*™ for item data. This data can then be used by bot builders, taking away the need for everyone to collect and maintain that data separately. 

The tool is run hourly and commits the resulting json to this repository (see [data/resources.json](https://github.com/AVee/cw_wiki_sync/blob/master/data/resources.json)). To get recent data you can just fetch the [raw resources.json](https://raw.githubusercontent.com/AVee/cw_wiki_sync/master/data/resources.json) regularly (or checkout this repo and pull regularly). While not a full blown api it probably is enough to serve the need of bot builders.

If any item data is missing or incomplete please just edit the wiki, it has a really nice form for editing item information ;-) Really, just go and improve what is on the wiki, the quality of this data depends on contributions to the wiki from users like you...

## Notes on resources.json
The intention is to keep the the file backwards compatible whenever possible. So new fields may be added, but existing fields will not be changed or removed. There are two top flags in the file indicating it's status, `deprecated` and `obsolete`. If the deprecated flag is set to true this indicates there is a newer format available and support for this version of the file will end at some point. If the obsolete becomes true the file is no longer automatically updated and the new version must be used to get the most recent data.

All known values for certain fields are included in the file, null values are not included. This means missing keys should generally be considered unknown (or not applicable).

There are two collections in the file, the first being 'items', which contains all valid items. The second is the 'incomplete' collection which contains all items for which the ID is missing. Separating these allows users of the json file to just work with the complete items and ignore work-in-progress items when new stuff is released in Chatwars.

## Running
The code is developed against Python 3.7, older Python 3 versions might work but there a no guarantees. A requirements.txt file is so dependancies can be installed with `pip3 install -r requirements.txt`

## Item data
If you currently have item data in some structured format which contains information missing on the wiki let me know (either in a issue here or contact @AVee00 on Telegram). It might be possible to import this data into the items on the wiki.

## Development
I use PyDev in Eclipse, but it's a plain pain Python project so it should be no problem to work with it using whatever tool you prefer. Pull requests are welcome.

## Roadmap
This is a spare-time project, so progress will very much depend on time available. But these are some possible feature goals:
- Create some tooling to scan for missing, incorrect or suspect values.
- Create a Telegram bot which:
  - Can parse relevent cw forwards and update the wiki.
  - Can present random 'things to fix' to users as a way to get issues resolved.
  - Can do so sort of consensus based editing of wiki data.
  - Monitors changes and reports them somewhere.
- Add other data such as:
  - Castle info
  - Guild levels
  - Class/skill info
  - ...

