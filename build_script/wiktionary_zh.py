from sqlite3 import Connection

WIKTIONARY_LANG_CODE = "zh"


def add_languages_with_variant(conn: Connection, lang_variant: str) -> None:
    from xml.etree import ElementTree

    from db import insert_data, lang_name_exists
    from mediawiki_api import mediawiki_api_request

    # https://zh.wiktionary.org/wiki/Wiktionary:语言列表
    page_html = mediawiki_api_request(
        WIKTIONARY_LANG_CODE,
        {
            "action": "parse",
            "page": "Wiktionary:语言列表",
            "prop": "text",
            "variant": lang_variant,
        },
        ("parse", "text"),
    )
    root = ElementTree.fromstring(page_html)
    for table in root.iterfind(".//table"):
        for tr_tag in table.iterfind(".//tr"):
            lang_code = ""
            for index, td_tag in enumerate(tr_tag.iterfind("td")):
                td_text = "".join(td_tag.itertext()).strip()
                if len(td_text) == 0:
                    continue
                if index == 0:
                    lang_code = td_text
                elif index == 1 and not lang_name_exists(conn, td_text):
                    # Chinese Wiktionary's Lua code are copied from English Wiktionary
                    # some language names are not translated, don't add again
                    insert_data(conn, lang_code, td_text, WIKTIONARY_LANG_CODE)
                elif index == 4:
                    for other_name in filter(None, td_text.split(", ")):
                        if not lang_name_exists(conn, other_name):
                            insert_data(
                                conn, lang_code, other_name, WIKTIONARY_LANG_CODE
                            )


def add_zh_wiktionary_languages(conn: Connection) -> None:
    from db import insert_data

    for lang_variant in ("", "zh-hant", "zh-hans"):
        add_languages_with_variant(conn, lang_variant)

    for lang_code, lang_names in EXTRA_LANG_NAMES.items():
        for lang_name in lang_names:
            insert_data(conn, lang_code, lang_name, WIKTIONARY_LANG_CODE)


EXTRA_LANG_NAMES = {
    "ace": ["亚齐語"],
    "af": ["阿非利堪斯語", "阿非利堪斯语"],
    "bho": ["博傑普爾語"],
    "bs": ["波斯尼亚语"],
    "ca": ["加泰罗尼亚語"],
    "chg": ["察合台語"],
    "cic": ["契卡索語"],
    "crx": ["卡列爾語"],
    "en": ["英文"],
    "frr": ["北弗里西語", "北弗里西语", "北弗類西語"],
    "gmw-cfr": ["中法蘭克尼亞語"],
    "got": ["哥德語"],
    "he": ["希伯来語"],
    "hr": ["克罗地亚语"],
    "hrx": ["亨斯里克語"],
    "ia": ["國際語", "国际语"],
    "id": ["印度尼西亞語", "印度尼西亚语"],
    "it": ["義大利語"],
    "ja": ["日文"],
    "ka": ["格鲁吉亞語"],
    "kmr": ["北庫德語"],
    "ko": ["韓語", "韩语"],
    "kpv": ["兹梁科米語"],
    "kxd": ["文萊馬來語"],
    "ms": ["馬来語"],
    "mt": ["馬耳他語", "马耳他语"],
    "mul": ["多語言", "多语言", "漢字", "跨语言词"],
    "my": ["缅甸語"],
    "nan": ["閩語"],
    "oc": ["奧克西唐語"],
    "oge": ["古格魯吉亞語"],
    "ojp": ["古日語", "古日语"],
    "or": ["奧里亞語"],
    "osx": ["古薩克遜語"],
    "ota": ["奧圖曼土耳其語", "奧斯曼土耳其語"],
    "se": ["北方薩米語"],
    "si": ["僧伽羅語"],
    "smn": ["伊纳里薩米語"],
    "stq": ["沙特弗里西語"],
    "sw": ["斯瓦西里語"],
    "ti": ["提格利尼亞語"],
    "tl": ["塔加洛語", "塔加洛语", "塔加祿語"],
    "tpw": ["古典圖皮語"],
    "txg": ["西夏文"],
    "udm": ["烏德穆爾特語"],
    "uz": ["烏茲别克語"],
    "wbm": ["佤族语"],
    "xcl": ["古亞美尼亞語", "古亚美尼亚语"],
    "xno": ["盎格鲁-诺曼语"],
    "yi": ["意第绪語"],
    "za": ["壮語"],
    "zgh": ["標準摩洛哥柏柏語"],
    "zh": ["中文"],
}
