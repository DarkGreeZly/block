import eth_keys
import os
import hashlib
import time


class Block:
    block_num = 0
    def __init__(self, prev_hash, data):
        self.data = data
        self.prev_hash = prev_hash
        self.nonce = 0
        self.timestamp = time.time()
        Block.block_num += 1
        self.block_number = Block.block_num
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.data).encode('utf-8') +
                   str(self.prev_hash).encode('utf-8') +
                   str(self.nonce).encode('utf-8'))
        return sha.hexdigest()

    def proof_of_work(self, difficulty: int):
        while self.hash[0:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print("Mined: " + self.hash)

    @classmethod
    def get_block_num(cls):
        return cls.block_number


class BlockChain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    @staticmethod
    def create_genesis_block():
        return Block("0", "Genesis Block")

    def add_block(self, new_block: Block, difficulty):
        new_block.prev_hash = self.chain[-1]
        new_block.proof_of_work(difficulty)
        self.chain.append(new_block)


def ecdsa_sign(message):
    private_key = eth_keys.keys.PrivateKey(os.urandom(32))
    public_key = private_key.public_key
    print("Private Key: ", private_key)
    print("Public Key: ", public_key)

    message = str(message).encode('utf-8')
    signature = private_key.sign_msg(message)
    print("Message: " + message.decode())
    print("Signature:\n"
          f"r = {hex(signature.r)}\n"
          f"s = {hex(signature.s)}\n"
          f"v = {hex(signature.v)}")
    valid = public_key.verify_msg(message, signature)
    print("Signature valid: ", valid)


if __name__ == "__main__":
    blockchain = BlockChain()
    block1 = Block("", {"sender": "David", "recipient": "Bob", "amount": 4})
    blockchain.add_block(block1, 1)
    block2 = Block("", {"sender": "Bob", "recipient": "Ann", "amount": 3.1})
    blockchain.add_block(block2, 1)
    block3 = Block("", {"sender": "Ann", "recipient": "David", "amount": 2.2})
    blockchain.add_block(block3, 1)
    for block in blockchain.chain:
        print(f"Block number: {block.block_number}\n"
              f"Transaction: {block.data}\n"
              f"{ecdsa_sign(block.data)}")