from typing import Any


def mediawiki_api_request(
    sub_domain: str, params: dict[str, str], result_keys: tuple[str, ...]
) -> Any:
    import requests

    params.update({"format": "json", "formatversion": "2"})
    r = requests.get(
        f"https://{sub_domain}.wiktionary.org/w/api.php",
        params=params,
        headers={"user-agent": "mediawiki_langcodes"},
    )
    data = r.json()
    for key in result_keys:
        data = data.get(key, {})
    return data
