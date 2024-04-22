from autotx.utils.ethereum import load_w3
from autotx.utils.ethereum.networks import NetworkInfo
from autotx.utils.ethereum.eth_address import ETHAddress

def test_swap_with_non_default_token(configuration, auto_tx):
    (_, _, _, manager) = configuration
    web3 = load_w3()
    network_info = NetworkInfo(web3.eth.chain_id)
    shib_address = ETHAddress(network_info.tokens["shib"])

    prompt = "Buy 100000 SHIB with ETH"
    balance = manager.balance_of(shib_address)
    assert balance == 0
    auto_tx.run(prompt, non_interactive=True)

    new_balance = manager.balance_of(shib_address)

    assert 100000 == new_balance

def test_swap_native(configuration, auto_tx):
    (_, _, _, manager) = configuration
    web3 = load_w3()
    network_info = NetworkInfo(web3.eth.chain_id)
    usdc_address = ETHAddress(network_info.tokens["usdc"])

    prompt = "Buy 100 USDC with ETH"
    balance = manager.balance_of(usdc_address)

    auto_tx.run(prompt, non_interactive=True)

    new_balance = manager.balance_of(usdc_address)

    assert balance + 100 == new_balance

def test_swap_multiple_1(configuration, auto_tx):
    (_, _, _, manager) = configuration
    web3 = load_w3()
    network_info = NetworkInfo(web3.eth.chain_id)
    usdc_address = ETHAddress(network_info.tokens["usdc"])
    wbtc_address = ETHAddress(network_info.tokens["wbtc"])

    prompt = "Buy 1000 USDC with ETH and then buy WBTC with 500 USDC"
    usdc_balance = manager.balance_of(usdc_address)
    wbtc_balance = manager.balance_of(wbtc_address)

    auto_tx.run(prompt, non_interactive=True)

    assert usdc_balance + 500 == manager.balance_of(usdc_address)
    assert wbtc_balance < manager.balance_of(wbtc_address)

def test_swap_multiple_2(configuration, auto_tx):
    (_, _, _, manager) = configuration
    web3 = load_w3()
    network_info = NetworkInfo(web3.eth.chain_id)
    usdc_address = ETHAddress(network_info.tokens["usdc"])
    wbtc_address = ETHAddress(network_info.tokens["wbtc"])

    prompt = "Sell ETH for 1000 USDC and then sell 500 USDC for WBTC"
    usdc_balance = manager.balance_of(usdc_address)
    wbtc_balance = manager.balance_of(wbtc_address)

    auto_tx.run(prompt, non_interactive=True)

    assert usdc_balance + 500 == manager.balance_of(usdc_address)
    assert wbtc_balance < manager.balance_of(wbtc_address)

def test_swap_triple(configuration, auto_tx): 
    (_, _, _, manager) = configuration
    web3 = load_w3()
    network_info = NetworkInfo(web3.eth.chain_id)
    usdc_address = ETHAddress(network_info.tokens["usdc"])
    uni_address = ETHAddress(network_info.tokens["uni"])
    wbtc_address = ETHAddress(network_info.tokens["wbtc"])

    prompt = "Buy 1 USDC, 0.5 UNI and 0.05 WBTC with ETH"
    usdc_balance = manager.balance_of(usdc_address)
    uni_balance = manager.balance_of(uni_address)
    wbtc_balance = manager.balance_of(wbtc_address)

    auto_tx.run(prompt, non_interactive=True)

    assert usdc_balance + 1 == manager.balance_of(usdc_address)
    assert uni_balance + 0.5 == manager.balance_of(uni_address)
    assert wbtc_balance + 0.05 == manager.balance_of(wbtc_address)

def test_swap_complex_1(configuration, auto_tx): # This one is complex because it confuses the LLM with WBTC amount
    (_, _, _, manager) = configuration
    web3 = load_w3()
    network_info = NetworkInfo(web3.eth.chain_id)
    usdc_address = ETHAddress(network_info.tokens["usdc"])
    wbtc_address = ETHAddress(network_info.tokens["wbtc"])

    prompt = "Swap ETH to 0.05 WBTC, then, swap WBTC to 1000 USDC"
    usdc_balance = manager.balance_of(usdc_address)
    wbtc_balance = manager.balance_of(wbtc_address)

    auto_tx.run(prompt, non_interactive=True)

    assert usdc_balance + 1000 == manager.balance_of(usdc_address)
    assert wbtc_balance < manager.balance_of(wbtc_address)

def test_swap_complex_2(configuration, auto_tx): # This one is complex because it confuses the LLM with WBTC amount
    (_, _, _, manager) = configuration
    web3 = load_w3()
    network_info = NetworkInfo(web3.eth.chain_id)
    usdc_address = ETHAddress(network_info.tokens["usdc"])
    wbtc_address = ETHAddress(network_info.tokens["wbtc"])

    prompt = "Buy 1000 USDC with ETH, then sell the USDC to buy 0.001 WBTC"
    usdc_balance = manager.balance_of(usdc_address)
    wbtc_balance = manager.balance_of(wbtc_address)

    auto_tx.run(prompt, non_interactive=True)

    assert usdc_balance < manager.balance_of(usdc_address)
    assert wbtc_balance + 0.001 == manager.balance_of(wbtc_address)
