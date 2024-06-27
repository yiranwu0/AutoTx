import json
from textwrap import dedent
from typing import Union

from autotx.utils import http_requests

KLEROS_TOKENS_LIST = "https://t2crtokens.eth.link/"
COINGECKO_TOKENS_LISTS = [
    "https://tokens.coingecko.com/uniswap/all.json",
    "https://tokens.coingecko.com/optimistic-ethereum/all.json",
    "https://tokens.coingecko.com/polygon-pos/all.json",
    "https://tokens.coingecko.com/base/all.json",
    "https://tokens.coingecko.com/arbitrum-one/all.json",
    "https://tokens.coingecko.com/xdai/all.json",
    "https://tokens.coingecko.com/zksync/all.json",
]


TOKENS_LIST = [KLEROS_TOKENS_LIST, *COINGECKO_TOKENS_LISTS]


async def fetch_tokens_list() -> None:
    loaded_tokens: list[dict[str, Union[str, int]]] = []

    for token_list_url in TOKENS_LIST:
        try:
            response = await http_requests.get(token_list_url)
            result = await response.json()
            tokens = result["tokens"]
            loaded_tokens.extend(tokens)
        except:
            print("Error while trying to fetch list:", token_list_url)

    loaded_tokens_as_string = json.dumps(loaded_tokens, indent=2)
    content = dedent(
        f"""# THIS IS AN AUTOGENERATED FILE. DO NOT MODIFY MANUALLY, PLEASE CHECK autotx/load_tokens.py TO DO ANY MODIFICATIONS

token_list = {loaded_tokens_as_string}
"""
    )
    with open("autotx/utils/ethereum/helpers/token_list.py", "w") as f:
        f.write(content)


async def run() -> None:
    await fetch_tokens_list()
