import hashlib
import time
import json
from typing import List, Dict

class Block:
    def __init__(self, index: int, previous_hash: str, timestamp: int, transactions: List[Dict], nonce: int = 0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.mining_reward = 1
        self.nodes = set()

    def create_genesis_block(self) -> Block:
        return Block(0, "0", int(time.time()), [], 0)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def mine_block(self, miner_address: str) -> Block:
        self.pending_transactions.append({
            "sender": "0",
            "recipient": miner_address,
            "amount": self.mining_reward
        })

        block = Block(len(self.chain), self.get_latest_block().hash,
                      int(time.time()), self.pending_transactions)

        block.nonce = self.proof_of_work(block)
        self.chain.append(block)
        self.pending_transactions = []
        return block

    def proof_of_work(self, block: Block) -> int:
        block.nonce = 0
        computed_hash = block.calculate_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.calculate_hash()
        return block.nonce

    def add_transaction(self, sender: str, recipient: str, amount: float) -> int:
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })
        return self.get_latest_block().index + 1

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

            if not self.is_valid_proof(current_block, current_block.hash):
                return False

        return True

    def is_valid_proof(self, block: Block, block_hash: str) -> bool:
        return (block_hash.startswith('0' * self.difficulty) and
                block_hash == block.calculate_hash())

    def resolve_conflicts(self) -> bool:
        neighbors = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbors:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def register_node(self, address: str):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

blockchain = Blockchain()
