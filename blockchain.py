import hashlib
import json
import time
import os

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
        self.filename = "blockchain_data.json"
        self.chain = []
        if os.path.exists(self.filename):
            self.load()
        else:
            self.chain = [self.create_genesis_block()]
            self.save()

    def create_genesis_block(self):
        return Block(0, time.time(), {"info": "Genesis Block"}, "0")

    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), time.time(), data, last_block.hash)
        self.chain.append(new_block)
        self.save()

    def save(self):
        with open(self.filename, "w") as f:
            json.dump([block.__dict__ for block in self.chain], f, indent=2)

    def load(self):
        with open(self.filename, "r") as f:
            blocks = json.load(f)
            self.chain = []
            for b in blocks:
                block = Block(
                    b['index'],
                    b['timestamp'],
                    b['data'],
                    b['previous_hash']
                )
                block.hash = b['hash']
                self.chain.append(block)

    def get_all_products(self):
        return [block.data for block in self.chain if block.index > 0]

    def get_product_by_id(self, pid):
        for block in self.chain:
            if block.index > 0 and block.data.get("product_id") == pid:
                return block.data
        return None
