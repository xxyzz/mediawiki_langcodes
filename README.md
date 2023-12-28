# MediaWiki langcodes

Convert MediaWiki language names and language codes.

## Build dependencies

- php

- wget

## Build

```
$ python -m venv .venv
$ source .venv/bin/activate.fish
$ python -m pip install -U pip build
$ make
```

### Update extra language names

Extract language names from Lua modules in the Wiktionary dump file,
use code from https://github.com/tatuylonen/wiktextract/blob/master/languages/get_data.py

```
$ python languages/get_data.py en --db-file ../en_20231220.db
$ python languages/get_data.py zh --db-file ../zh_20231220.db
```

then in this project folder:

```
// download files
$ make lang_files
// remove old extra files
$ rm build_script/extra_names/*.json
// create a db file without extra languages
$ python build_script/main.py
$ python build_script/add_extra.py en path_to_en_extra_json
// add extra languages from the English Wiktionary
$ python build_script/main.py
$ python build_script/add_extra.py zh path_to_zh_extra_json
```

## Usage

```python
from mediawiki_langcodes import code_to_name, name_to_code

code_to_name("fr")  # return "français"
code_to_name("fr", "en")  # return "French"
name_to_code("français")  # return "fr"
name_to_code("français", "fr")  # return "fr"
```
