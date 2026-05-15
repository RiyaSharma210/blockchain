import hashlib
import json
from time import time
from datetime import datetime


class Blockchain:

    def __init__(self):

        self.chain = []

        self.fake_detected = 0

        self.create_block(previous_hash='0')


    # =========================
    # CREATE BLOCK
    # =========================

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


    # =========================
    # HASH FUNCTION
    # =========================

    def hash(self, block):

        encoded_block = json.dumps(
            block,
            sort_keys=True
        ).encode()

        return hashlib.sha256(
            encoded_block
        ).hexdigest()


    # =========================
    # GET PREVIOUS BLOCK
    # =========================

    def get_previous_block(self):

        return self.chain[-1]


    # =========================
    # BLOCKCHAIN STATISTICS
    # =========================

    def get_statistics(self):

        total_products = len(self.chain) - 1

        total_blocks = len(self.chain)

        return {

            'total_products': total_products,

            'total_blocks': total_blocks,

            'genuine_products': total_products,

            'fake_detected': self.fake_detected
        }


    # =========================
    # VERIFICATION HISTORY
    # =========================

    def get_history(self):

        history = []

        for block in reversed(self.chain[1:]):

            data = block['product_data']

            if data:

                history.append({

                    'product_name': data['product_name'],

                    'manufacturer': data['manufacturer'],

                    'product_id': data['product_id']
                })

        return history


    # =========================
    # VERIFY PRODUCT
    # =========================

    def verify_product(self, product_name):

        for block in self.chain:

            data = block['product_data']

            if data:

                if data['product_name'].lower() == product_name.lower():

                    return {

                        'found': True,

                        'product_name': data['product_name'],

                        'manufacturer': data['manufacturer'],

                        'product_id': data['product_id'],

                        'manufacturing_date': data['manufacturing_date'],

                        'image': data['image'],

                        'hash': block['hash'],

                        'verified_at': datetime.now().strftime(
                            "%d-%m-%Y %I:%M:%S %p"
                        )
                    }

        # INCREASE FAKE DETECTION COUNT

        self.fake_detected += 1

        return {

            'found': False
        }