MEDIAWIKI_TAG := 1.43.0
MEDIAWIKI_CLDR_TAG := 2025.03
CLDR_TAG := release-47

DB_PATH := src/mediawiki_langcodes/langcodes.db

build: $(DB_PATH)
	python -m build

$(DB_PATH): lang_files
	python build_script/main.py

lang_files: \
	build/mediawiki-extensions-cldr-$(MEDIAWIKI_CLDR_TAG) \
	build/mediawiki-$(MEDIAWIKI_TAG) \
	build/cldr-$(CLDR_TAG)

define download_tag
	wget -nv -P build "https://github.com/$1/archive/refs/tags/$2.tar.gz"
	tar -xf build/$2.tar.gz -C build
	rm build/$2.tar.gz
endef

define download_branch
	wget -nv -P build "https://github.com/$1/archive/refs/heads/$2.zip"
	unzip -d build build/$2.zip
	rm build/$2.zip
endef

build/mediawiki-$(MEDIAWIKI_TAG):
	$(call download_tag,wikimedia/mediawiki,$(MEDIAWIKI_TAG))

build/mediawiki-extensions-cldr-$(MEDIAWIKI_CLDR_TAG):
	$(call download_tag,wikimedia/mediawiki-extensions-cldr,$(MEDIAWIKI_CLDR_TAG))

build/cldr-$(CLDR_TAG):
	$(call download_tag,unicode-org/cldr,$(CLDR_TAG))

.PHONY: clean
clean:
	rm -rf build
	rm $(DB_PATH)
	rm -rf dist

test:
	python -m unittest discover -s tests
