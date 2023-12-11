MEDIAWIKI_TAG := 1.40.1
MEDIAWIKI_CLDR_TAG := 2023.12
CLDR_TAG := release-44-1

DB_PATH := src/mediawiki_langcodes/langcodes.db

build: $(DB_PATH)
	python -m build

$(DB_PATH): lang_files
	python build_script/main.py

lang_files: \
	build/mediawiki-extensions-cldr-$(MEDIAWIKI_CLDR_TAG) \
	build/mediawiki-$(MEDIAWIKI_TAG) \
	build/cldr-$(CLDR_TAG)

define download_file
	wget -nv -P build "https://github.com/$1/archive/refs/tags/$2.tar.gz"
	tar -xf build/$2.tar.gz -C build
	rm build/$2.tar.gz
endef

build/mediawiki-$(MEDIAWIKI_TAG):
	$(call download_file,wikimedia/mediawiki,$(MEDIAWIKI_TAG))

build/mediawiki-extensions-cldr-$(MEDIAWIKI_CLDR_TAG):
	$(call download_file,wikimedia/mediawiki-extensions-cldr,$(MEDIAWIKI_CLDR_TAG))

build/cldr-$(CLDR_TAG):
	$(call download_file,unicode-org/cldr,$(CLDR_TAG))

.PHONY: clean
clean:
	rm -rf build
	rm $(DB_PATH)
	rm -rf dist

test:
	python -m unittest discover -s tests
