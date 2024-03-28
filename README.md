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

## Usage

```python
from mediawiki_langcodes import code_to_name, name_to_code

code_to_name("fr")  # return "français"
code_to_name("fr", "en")  # return "French"
name_to_code("français")  # return "fr"
name_to_code("français", "fr")  # return "fr"
```
