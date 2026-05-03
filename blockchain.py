import hashlib
import json
from time import time

class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(previous_hash='0')

    def create_block(self, product_data=None, previous_hash='0'):

        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(time()),
            'product_data': product_data,
            'previous_hash': previous_hash
        }

        block['hash'] = self.hash(block)

        self.chain.append(block)

        return block

    def hash(self, block):

        encoded_block = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(encoded_block).hexdigest()

    def get_previous_block(self):
        return self.chain[-1]

    def verify_product(self, product_name):

        for block in self.chain:

            data = block['product_data']

            if data:

                if data['product_name'].lower() == product_name.lower():

                    return {
                        'found': True,
                        'manufacturer': data['manufacturer'],
                        'hash': block['hash']
                    }

        return {
            'found': False
        }