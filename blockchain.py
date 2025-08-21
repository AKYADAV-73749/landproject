import hashlib
import json
import time
from datetime import datetime

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate the hash of the block"""
        block_string = json.dumps({
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """Mine the block with proof of work"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

class Transaction:
    def __init__(self, from_address, to_address, land_id, transaction_type, details=None):
        self.from_address = from_address
        self.to_address = to_address
        self.land_id = land_id
        self.transaction_type = transaction_type  # 'register', 'transfer'
        self.details = details or {}
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            "from_address": self.from_address,
            "to_address": self.to_address,
            "land_id": self.land_id,
            "transaction_type": self.transaction_type,
            "details": self.details,
            "timestamp": self.timestamp
        }

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions = []
        self.mining_reward = 100
    
    def create_genesis_block(self):
        """Create the first block in the blockchain"""
        return Block(0, [], time.time(), "0")
    
    def get_latest_block(self):
        """Get the latest block in the chain"""
        return self.chain[-1]
    
    def add_transaction(self, transaction):
        """Add a transaction to pending transactions"""
        self.pending_transactions.append(transaction.to_dict())
    
    def mine_pending_transactions(self, mining_reward_address):
        """Mine all pending transactions"""
        reward_transaction = {
            "from_address": None,
            "to_address": mining_reward_address,
            "land_id": None,
            "transaction_type": "mining_reward",
            "details": {"amount": self.mining_reward},
            "timestamp": datetime.now().isoformat()
        }
        
        self.pending_transactions.append(reward_transaction)
        
        block = Block(
            len(self.chain),
            self.pending_transactions,
            time.time(),
            self.get_latest_block().hash
        )
        
        block.mine_block(self.difficulty)
        
        print("Block successfully mined!")
        self.chain.append(block)
        self.pending_transactions = []
    
    def get_balance(self, address):
        """Get balance for an address (for future token implementation)"""
        balance = 0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.get('from_address') == address:
                    balance -= transaction.get('details', {}).get('amount', 0)
                
                if transaction.get('to_address') == address:
                    balance += transaction.get('details', {}).get('amount', 0)
        
        return balance
    
    def get_land_history(self, land_id):
        """Get complete history of a land parcel"""
        history = []
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.get('land_id') == land_id:
                    history.append({
                        "block_index": block.index,
                        "transaction": transaction,
                        "block_hash": block.hash
                    })
        
        return history
    
    def get_current_owner(self, land_id):
        """Get current owner of a land parcel"""
        current_owner = None
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.get('land_id') == land_id:
                    if transaction.get('transaction_type') in ['register', 'transfer']:
                        current_owner = transaction.get('to_address')
        
        return current_owner
    
    def is_chain_valid(self):
        """Validate the blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_all_transactions(self):
        """Get all transactions from the blockchain"""
        all_transactions = []
        
        for block in self.chain:
            for transaction in block.transactions:
                transaction_with_block = transaction.copy()
                transaction_with_block['block_index'] = block.index
                transaction_with_block['block_hash'] = block.hash
                all_transactions.append(transaction_with_block)
        
        return all_transactions
    
    def to_dict(self):
        """Convert blockchain to dictionary for JSON serialization"""
        return {
            "chain": [
                {
                    "index": block.index,
                    "transactions": block.transactions,
                    "timestamp": block.timestamp,
                    "previous_hash": block.previous_hash,
                    "hash": block.hash,
                    "nonce": block.nonce
                }
                for block in self.chain
            ],
            "difficulty": self.difficulty,
            "pending_transactions": self.pending_transactions
        }
