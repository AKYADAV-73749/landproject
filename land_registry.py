import json
import os
from datetime import datetime
from templates.blockchain import Blockchain, Transaction

class LandRegistry:
    def __init__(self, blockchain_file='blockchain_data.json'):
        self.blockchain = Blockchain()
        self.blockchain_file = blockchain_file
        self.load_blockchain()
    
    def load_blockchain(self):
        """Load blockchain from file if it exists"""
        if os.path.exists(self.blockchain_file):
            try:
                with open(self.blockchain_file, 'r') as f:
                    data = json.load(f)
                    # Reconstruct blockchain from saved data
                    # For simplicity, we'll start fresh each time
                    # In production, you'd properly reconstruct the chain
                    pass
            except Exception as e:
                print(f"Error loading blockchain: {e}")
    
    def save_blockchain(self):
        """Save blockchain to file"""
        try:
            with open(self.blockchain_file, 'w') as f:
                json.dump(self.blockchain.to_dict(), f, indent=2)
        except Exception as e:
            print(f"Error saving blockchain: {e}")
    
    def register_land(self, land_id, owner_name, owner_address, land_details):
        """Register a new land parcel"""
        # Check if land already exists
        current_owner = self.blockchain.get_current_owner(land_id)
        if current_owner:
            return {
                "success": False,
                "message": f"Land {land_id} is already registered to {current_owner}"
            }
        
        # Create registration transaction
        transaction = Transaction(
            from_address="SYSTEM",
            to_address=owner_address,
            land_id=land_id,
            transaction_type="register",
            details={
                "owner_name": owner_name,
                "land_details": land_details,
                "registration_date": datetime.now().isoformat()
            }
        )
        
        # Add transaction to blockchain
        self.blockchain.add_transaction(transaction)
        self.blockchain.mine_pending_transactions("SYSTEM")
        self.save_blockchain()
        
        return {
            "success": True,
            "message": f"Land {land_id} successfully registered to {owner_name}",
            "transaction_hash": self.blockchain.get_latest_block().hash
        }
    
    def transfer_land(self, land_id, from_owner, to_owner, to_owner_name, transfer_details):
        """Transfer land ownership"""
        # Check if land exists
        current_owner = self.blockchain.get_current_owner(land_id)
        if not current_owner:
            return {
                "success": False,
                "message": f"Land {land_id} is not registered"
            }
        
        # Check if from_owner is the current owner
        if current_owner != from_owner:
            return {
                "success": False,
                "message": f"Only the current owner ({current_owner}) can transfer this land"
            }
        
        # Create transfer transaction
        transaction = Transaction(
            from_address=from_owner,
            to_address=to_owner,
            land_id=land_id,
            transaction_type="transfer",
            details={
                "new_owner_name": to_owner_name,
                "transfer_details": transfer_details,
                "transfer_date": datetime.now().isoformat()
            }
        )
        
        # Add transaction to blockchain
        self.blockchain.add_transaction(transaction)
        self.blockchain.mine_pending_transactions("SYSTEM")
        self.save_blockchain()
        
        return {
            "success": True,
            "message": f"Land {land_id} successfully transferred to {to_owner_name}",
            "transaction_hash": self.blockchain.get_latest_block().hash
        }
    
    def get_land_info(self, land_id):
        """Get current information about a land parcel"""
        current_owner = self.blockchain.get_current_owner(land_id)
        if not current_owner:
            return {
                "success": False,
                "message": f"Land {land_id} is not registered"
            }
        
        history = self.blockchain.get_land_history(land_id)
        
        # Get current owner details from the latest transaction
        current_details = {}
        for record in reversed(history):
            transaction = record['transaction']
            if transaction.get('transaction_type') in ['register', 'transfer']:
                current_details = transaction.get('details', {})
                break
        
        return {
            "success": True,
            "land_id": land_id,
            "current_owner": current_owner,
            "current_details": current_details,
            "transaction_count": len(history),
            "history": history
        }
    
    def get_all_lands(self):
        """Get information about all registered lands"""
        all_transactions = self.blockchain.get_all_transactions()
        lands = {}
        
        for transaction in all_transactions:
            land_id = transaction.get('land_id')
            if land_id and transaction.get('transaction_type') in ['register', 'transfer']:
                if land_id not in lands:
                    lands[land_id] = {
                        "land_id": land_id,
                        "current_owner": transaction.get('to_address'),
                        "registration_date": None,
                        "last_transfer_date": None,
                        "transaction_count": 0
                    }
                
                lands[land_id]['current_owner'] = transaction.get('to_address')
                lands[land_id]['transaction_count'] += 1
                
                if transaction.get('transaction_type') == 'register':
                    lands[land_id]['registration_date'] = transaction.get('details', {}).get('registration_date')
                elif transaction.get('transaction_type') == 'transfer':
                    lands[land_id]['last_transfer_date'] = transaction.get('details', {}).get('transfer_date')
        
        return list(lands.values())
    
    def verify_blockchain_integrity(self):
        """Verify the integrity of the blockchain"""
        return self.blockchain.is_chain_valid()
    
    def get_blockchain_stats(self):
        """Get blockchain statistics"""
        all_transactions = self.blockchain.get_all_transactions()
        
        stats = {
            "total_blocks": len(self.blockchain.chain),
            "total_transactions": len(all_transactions),
            "total_lands_registered": 0,
            "total_transfers": 0,
            "blockchain_valid": self.verify_blockchain_integrity()
        }
        
        for transaction in all_transactions:
            if transaction.get('transaction_type') == 'register':
                stats['total_lands_registered'] += 1
            elif transaction.get('transaction_type') == 'transfer':
                stats['total_transfers'] += 1
        
        return stats
