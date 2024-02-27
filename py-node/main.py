# import the following dependencies
import json
from web3 import Web3
import sqlite3
import asyncio
from starknet_py.contract import Contract
from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.hash.address import get_checksum_address
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_models import Call

from starknet_py.cairo.felt import decode_shortstring, encode_shortstring

# add your blockchain connection information
infura_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(infura_url))

# uniswap address and abi
# uniswap_router = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
contract = "0x68B1D87F95878fE05B998F19b66F4baba5De1aed"
contract_abi = json.loads(
    '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"target","type":"address"}],"name":"AddressEmptyCode","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"AddressInsufficientBalance","type":"error"},{"inputs":[],"name":"FailedInnerCall","type":"error"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"SafeERC20FailedOperation","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"beneficiary","type":"string"},{"indexed":false,"internalType":"uint256","name":"amount_in","type":"uint256"},{"indexed":true,"internalType":"address","name":"asset_in","type":"address"},{"indexed":false,"internalType":"string","name":"asset_out","type":"string"},{"indexed":false,"internalType":"uint256","name":"min_amount_out","type":"uint256"}],"name":"Swap","type":"event"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"reserves","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"new_owner","type":"address"}],"name":"setOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"beneficiary","type":"string"},{"internalType":"uint256","name":"amount_in","type":"uint256"},{"internalType":"address","name":"asset_in","type":"address"},{"internalType":"string","name":"asset_out","type":"string"},{"internalType":"uint256","name":"min_amount_out","type":"uint256"}],"name":"swap","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
)

contract = web3.eth.contract(address=contract, abi=contract_abi)


# define function to handle events and print to the console
async def handle_event(event):
    data = json.loads(Web3.to_json(event))
    print(data)
    # print(Web3.to_text(data['args']['beneficiary']))
    recipient = data["args"]["beneficiary"]
    hash = data["transactionHash"]

    conn = sqlite3.connect("events.db")
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY)")
    conn.commit()

    
    res = c.execute(f"SELECT * FROM events WHERE event_id=\"{hash}\"")
    resp = res.fetchall()
    print(resp)
    print(hash)

    if len(resp) != 0:
        print("Existing txn")
        return
    
    c.execute(f"INSERT INTO events (event_id) VALUES (\"{hash}\")")
    conn.commit()

    client = FullNodeClient(node_url="http://0.0.0.0:5050")
    # abi='[{"type":"struct","name":"core::integer::u256","members":[{"name":"low","type":"core::integer::u128"},{"name":"high","type":"core::integer::u128"}]},{"type":"function","name":"burn","inputs":[{"name":"value","type":"core::integer::u256"}],"outputs":[],"state_mutability":"external"},{"type":"function","name":"mint","inputs":[{"name":"recipient","type":"core::starknet::contract_address::ContractAddress"},{"name":"amount","type":"core::integer::u256"}],"outputs":[],"state_mutability":"external"},{"type":"impl","name":"ERC20MetadataImpl","interface_name":"openzeppelin::token::erc20::interface::IERC20Metadata"},{"type":"interface","name":"openzeppelin::token::erc20::interface::IERC20Metadata","items":[{"type":"function","name":"name","inputs":[],"outputs":[{"type":"core::felt252"}],"state_mutability":"view"},{"type":"function","name":"symbol","inputs":[],"outputs":[{"type":"core::felt252"}],"state_mutability":"view"},{"type":"function","name":"decimals","inputs":[],"outputs":[{"type":"core::integer::u8"}],"state_mutability":"view"}]},{"type":"impl","name":"ERC20Impl","interface_name":"openzeppelin::token::erc20::interface::IERC20"},{"type":"enum","name":"core::bool","variants":[{"name":"False","type":"()"},{"name":"True","type":"()"}]},{"type":"interface","name":"openzeppelin::token::erc20::interface::IERC20","items":[{"type":"function","name":"total_supply","inputs":[],"outputs":[{"type":"core::integer::u256"}],"state_mutability":"view"},{"type":"function","name":"balance_of","inputs":[{"name":"account","type":"core::starknet::contract_address::ContractAddress"}],"outputs":[{"type":"core::integer::u256"}],"state_mutability":"view"},{"type":"function","name":"allowance","inputs":[{"name":"owner","type":"core::starknet::contract_address::ContractAddress"},{"name":"spender","type":"core::starknet::contract_address::ContractAddress"}],"outputs":[{"type":"core::integer::u256"}],"state_mutability":"view"},{"type":"function","name":"transfer","inputs":[{"name":"recipient","type":"core::starknet::contract_address::ContractAddress"},{"name":"amount","type":"core::integer::u256"}],"outputs":[{"type":"core::bool"}],"state_mutability":"external"},{"type":"function","name":"transfer_from","inputs":[{"name":"sender","type":"core::starknet::contract_address::ContractAddress"},{"name":"recipient","type":"core::starknet::contract_address::ContractAddress"},{"name":"amount","type":"core::integer::u256"}],"outputs":[{"type":"core::bool"}],"state_mutability":"external"},{"type":"function","name":"approve","inputs":[{"name":"spender","type":"core::starknet::contract_address::ContractAddress"},{"name":"amount","type":"core::integer::u256"}],"outputs":[{"type":"core::bool"}],"state_mutability":"external"}]},{"type":"impl","name":"ERC20CamelOnlyImpl","interface_name":"openzeppelin::token::erc20::interface::IERC20CamelOnly"},{"type":"interface","name":"openzeppelin::token::erc20::interface::IERC20CamelOnly","items":[{"type":"function","name":"totalSupply","inputs":[],"outputs":[{"type":"core::integer::u256"}],"state_mutability":"view"},{"type":"function","name":"balanceOf","inputs":[{"name":"account","type":"core::starknet::contract_address::ContractAddress"}],"outputs":[{"type":"core::integer::u256"}],"state_mutability":"view"},{"type":"function","name":"transferFrom","inputs":[{"name":"sender","type":"core::starknet::contract_address::ContractAddress"},{"name":"recipient","type":"core::starknet::contract_address::ContractAddress"},{"name":"amount","type":"core::integer::u256"}],"outputs":[{"type":"core::bool"}],"state_mutability":"external"}]},{"type":"impl","name":"OwnableImpl","interface_name":"openzeppelin::access::ownable::interface::IOwnable"},{"type":"interface","name":"openzeppelin::access::ownable::interface::IOwnable","items":[{"type":"function","name":"owner","inputs":[],"outputs":[{"type":"core::starknet::contract_address::ContractAddress"}],"state_mutability":"view"},{"type":"function","name":"transfer_ownership","inputs":[{"name":"new_owner","type":"core::starknet::contract_address::ContractAddress"}],"outputs":[],"state_mutability":"external"},{"type":"function","name":"renounce_ownership","inputs":[],"outputs":[],"state_mutability":"external"}]},{"type":"impl","name":"OwnableCamelOnlyImpl","interface_name":"openzeppelin::access::ownable::interface::IOwnableCamelOnly"},{"type":"interface","name":"openzeppelin::access::ownable::interface::IOwnableCamelOnly","items":[{"type":"function","name":"transferOwnership","inputs":[{"name":"newOwner","type":"core::starknet::contract_address::ContractAddress"}],"outputs":[],"state_mutability":"external"},{"type":"function","name":"renounceOwnership","inputs":[],"outputs":[],"state_mutability":"external"}]},{"type":"constructor","name":"constructor","inputs":[{"name":"owner","type":"core::starknet::contract_address::ContractAddress"}]},{"type":"event","name":"openzeppelin::token::erc20::erc20::ERC20Component::Transfer","kind":"struct","members":[{"name":"from","type":"core::starknet::contract_address::ContractAddress","kind":"key"},{"name":"to","type":"core::starknet::contract_address::ContractAddress","kind":"key"},{"name":"value","type":"core::integer::u256","kind":"data"}]},{"type":"event","name":"openzeppelin::token::erc20::erc20::ERC20Component::Approval","kind":"struct","members":[{"name":"owner","type":"core::starknet::contract_address::ContractAddress","kind":"key"},{"name":"spender","type":"core::starknet::contract_address::ContractAddress","kind":"key"},{"name":"value","type":"core::integer::u256","kind":"data"}]},{"type":"event","name":"openzeppelin::token::erc20::erc20::ERC20Component::Event","kind":"enum","variants":[{"name":"Transfer","type":"openzeppelin::token::erc20::erc20::ERC20Component::Transfer","kind":"nested"},{"name":"Approval","type":"openzeppelin::token::erc20::erc20::ERC20Component::Approval","kind":"nested"}]},{"type":"event","name":"openzeppelin::access::ownable::ownable::OwnableComponent::OwnershipTransferred","kind":"struct","members":[{"name":"previous_owner","type":"core::starknet::contract_address::ContractAddress","kind":"key"},{"name":"new_owner","type":"core::starknet::contract_address::ContractAddress","kind":"key"}]},{"type":"event","name":"openzeppelin::access::ownable::ownable::OwnableComponent::OwnershipTransferStarted","kind":"struct","members":[{"name":"previous_owner","type":"core::starknet::contract_address::ContractAddress","kind":"key"},{"name":"new_owner","type":"core::starknet::contract_address::ContractAddress","kind":"key"}]},{"type":"event","name":"openzeppelin::access::ownable::ownable::OwnableComponent::Event","kind":"enum","variants":[{"name":"OwnershipTransferred","type":"openzeppelin::access::ownable::ownable::OwnableComponent::OwnershipTransferred","kind":"nested"},{"name":"OwnershipTransferStarted","type":"openzeppelin::access::ownable::ownable::OwnableComponent::OwnershipTransferStarted","kind":"nested"}]},{"type":"event","name":"cairo_contract::UnichainX::Event","kind":"enum","variants":[{"name":"ERC20Event","type":"openzeppelin::token::erc20::erc20::ERC20Component::Event","kind":"flat"},{"name":"OwnableEvent","type":"openzeppelin::access::ownable::ownable::OwnableComponent::Event","kind":"flat"}]}]'
    key_pair = KeyPair.from_private_key("0x7a33487e3721ff0ab5da2135deba3992")
    account = Account(
        client=client,
        address="0x2bc52755a7a30e7589acafd8a363585d5f5913b732d0bc0150d9ef830a4d9fa",
        key_pair=key_pair,
        chain=StarknetChainId.GOERLI,
    )
    contract_addr = data["args"]["asset_out"]
    contract = await Contract.from_address(provider=account, address=contract_addr)

    invocation = await contract.functions["transfer"].invoke_v1(
        recipient=int(recipient, 16),
        amount=int((data["args"]["amount_in"] / 10)),
        max_fee=10000000000000000000,
    )

    await invocation.wait_for_acceptance()

    # # call = Call(
    # #     to_addr=contract_addr,
    # #     selector=get_selector_from_name("approve"),
    # #     calldata=["0x2bc52755a7a30e7589acafd8a363585d5f5913b732d0bc0150d9ef830a4d9fa", "0x2bc52755a7a30e7589acafd8a363585d5f5913b732d0bc0150d9ef830a4d9fa", data["args"]["amount_in"], data["args"]["amount_in"]]
    # # )

    # # y = await account.client.call_contract(call)
    # # print(y)

    # # call = Call(
    # #     to_addr=contract_addr,
    # #     selector=get_selector_from_name("transfer"),
    # #     calldata=[int("0x2bc52755a7a30e7589acafd8a363585d5f5913b732d0bc0150d9ef830a4d9fa", 16), data["args"]["amount_in"], data["args"]["amount_in"]],
    # # )

    # # x = await account.client.call_contract(call)
    # print(x)
    print("ok")


# data.args contains the arguments for the event
# these args are: beneficiary (bytes of the address to be sent to), amount_in (amount that was sent), asset_in (address of the erc20 contract sent)
# asset_out (bytes address of the starknet erc20 contract to be called)

# TODO: IMPORTANT! duplicate events are sent, so store the events in a database (use sqlite if you can) and ignore
# if the event was already picked up
# TODO: we're doing 10:1, so divide amount_in by 10 to get how much starknet tokens to be sent
# TODO: convert the hex bytes of the beneficiary and asset_out to string (use google for this, web3 hex to str)
# TODO: use starknet py to call the starknet smart contract to transfer tokens: first approve needs to be called,
# then transfer needs to be called to get the tokens to the beneficiary address


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for Swap in event_filter.get_new_entries():
            await handle_event(Swap)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    event_filter = contract.events.Swap.create_filter(fromBlock="latest")
    # block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(log_loop(event_filter, 2)))
        # log_loop(block_filter, 2),
        # log_loop(tx_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()


if __name__ == "__main__":
    main()
