from typing import Dict

from hexbytes import HexBytes

from ethtx_ce.backend.models.w3_model import W3Log, W3Transaction, W3Receipt, W3Block
from ethtx_ce.helpers import AttrDict


class MockMongoConnection:
    def get_semantics(self, chain_id, address):
        return {"name": "test", "events": "test"}

    def insert_contract(self, contract, update_if_exist=False):
        contract_with_id = {"_id": contract["chash"], **contract}

        if update_if_exist:
            self._contracts.replace_one(
                {"_id": contract_with_id["_id"]}, contract_with_id, upsert=True
            )
        else:
            self._contracts.insert_one(contract_with_id)

    def insert_address(self, address, update_if_exist=False):
        address_with_id = {
            "_id": f"{address['network']}-{address['address']}",
            **address,
        }

        if update_if_exist:
            self._addresses.replace_one(
                {"_id": address_with_id["_id"]}, address_with_id, upsert=True
            )
        else:
            self._addresses.insert_one(address_with_id)

    def insert_signature(self, signature, update_if_exist=False):
        signature_with_id = {"_id": signature["hash"], **signature}

        if update_if_exist:
            self._signatures.replace_one(
                {"_id": signature_with_id["_id"]}, signature_with_id, upsert=True
            )
        else:
            self._signatures.insert_one(signature_with_id)

    def get_contract(self, contract_code_hash):
        return []

    def get_address(self, network, address):
        return []

    def get_signature(self, signature_hash):
        return []


class MockWeb3Provider:
    blocks = {
        1: {
            "difficulty": 123,  # int
            "extraData": "test",  # HexBytes
            "gasLimit": 123,  # int
            "gasUsed": 123,  # int
            "hash": HexBytes(
                b"\x88\xe9mE7\xbe\xa4\xd9\xc0]\x12T\x99\x07\xb3%a\xd3\xbf1\xf4Z\xaesL\xdc\x11\x9f\x13@l\xb6"
            ),  # str
            "logsBloom": "test",  # HexBytes
            "miner": "test",  # str
            "nonce": "test",  # HexBytes
            "number": 123,  # int
            "parentHash": HexBytes(
                b"\x88\xe9mE7\xbe\xa4\xd9\xc0]\x12T\x99\x07\xb3%a\xd3\xbf1\xf4Z\xaesL\xdc\x11\x9f\x13@l\xb6"
            ),  # str
            "receiptsRoot": "test",  # HexBytes
            "sha3Uncles": "test",  # HexBytes
            "size": 123,  # int
            "stateRoot": "test",  # HexBytes
            "timestamp": 123,  # int,
            "totalDifficulty": 123,  # int
            "transactions": [],  # List
            "transactionsRoot": "test",  # HexBytes
            "uncles": [],  # List
        }
    }

    txs = {
        "0xd7701a0fc05593aee3a16f20cab605db7183f752ae942cc75fd0975feaf1072e": {
            "blockHash": HexBytes(
                b"\x88\xe9mE7\xbe\xa4\xd9\xc0]\x12T\x99\x07\xb3%a\xd3\xbf1\xf4Z\xaesL\xdc\x11\x9f\x13@l\xb6"
            ),  # str
            "blockNumber": 1,  # int
            "from_address": "fromasd",  # str
            "gas": 420,  # int
            "gasPrice": 1,  # int
            "hash": "co",  # HexBytes,
            "input": "jeszcze jak",  # str
            "nonce": 123,  # int
            "r": "ds",  # HexBytes
            "s": "sdf",  # HexBytes
            "to": "sdf",  # str
            "transactionIndex": 1,  # int
            "v": 1,  # int
            "value": 1,  # int
        }
    }

    def add_mocked_block_details(self, block_number, block_details: Dict):
        self.blocks[block_number] = block_details

    def get_transaction(self, tx_hash):
        return W3Transaction(**self.txs[tx_hash])

    def get_transaction_receipt(self, tx_hash):
        log_values = AttrDict(
            {
                "address": "test",  # str
                "blockHash": "test",  # HexBytes
                "blockNumber": 123,  # int
                "data": "test",  # str
                "logIndex": 132,  # int
                "removed": False,  # bool,
                "topics": [HexBytes("d")],  # List[HexBytes]
                "transactionHash": "test",  # HexBytes
                "transactionIndex": 123,  # int
            }
        )
        values = {
            "blockHash": "test",  # HexBytes
            "blockNumber": 123,  # int
            "contractAddress": 123,  # str
            "cumulativeGasUsed": 132,  # int,
            "from_address": "from",  # str
            "gasUsed": 123,  # int
            "logs": [log_values],  # List
            "logsBloom": "test",  # HexBytes
            "root": "test",  # str
            "status": 123,  # int,
            "to_address": "test",  # str
            "transactionHash": "test",  # HexBytes
            "transactionIndex": 123,  # int
        }
        return W3Receipt(**values)

    def get_block(self, block_number: int) -> W3Block:
        return W3Block(**self.blocks[block_number])


class MockSemanticsRepository:
    def get_event_abi(self, a, b, c):
        return ""

    def get_anonymous_event_abi(self, a, b):
        return ""

    def contract_name(self, a, b):
        return ""

    def contract_label(self, chain_id, contract):
        return ""


class Mocks:
    @staticmethod
    def get_mocked_w3_log():
        log_data = {
            "address": "test",
            "blockHash": "test_block_hash",
            "blockNumber": 123,
            "data": "data",
            "logIndex": 1,
            "removed": False,
            "topics": [1, 2, 3, 4],
            "transactionHash": "txHash",
            "transactionIndex": 1,
        }

        log = W3Log(**log_data)
        return log


class TestMocks:
    def test_can_create_w3_log(self):
        w3log = Mocks.get_mocked_w3_log()
        assert w3log is not None
