import hashlib
import json
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), {"info": "Genesis Block"}, "0")

    def add_block(self, data):
        prev = self.chain[-1]
        new = Block(len(self.chain), time.time(), data, prev.hash)
        self.chain.append(new)

    def get_all_products(self):
        return [block.data for block in self.chain if block.index > 0]

    def get_product_by_id(self, pid):
        for block in self.chain:
            if block.data.get("product_id") == pid:
                return block.data
        return None
