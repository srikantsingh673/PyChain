import hashlib # To create hashes for blocks
import time # To record the time when blocks are created

class PyChain:
    
    def __init__(self):
        self.chain = [] # This list will hold all blocks

        # Create the first block with proof=1 and previous_hash='0'
        self.create_block(proof=1, previous_hash='0')
        
        
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1, # Block number in the chain
            'timestamp': time.time(), #Time of creation
            'proof': proof, # Proof number to secure the block
            'previous_hash': previous_hash # Hash of the previous block
        }
        self.chain.append(block) # Add this block to the chain
        return block
    
    
    def get_previous_block(self):
        return self.chain[-1] # Return the last block in the chain
    
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while not check_proof:
            # Create a hash with the new proof and previous proof
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000': # Check if the hash starts with 4 zeros
                check_proof = True
            else:
                new_proof += 1 # Increment the proof and try again               
        return new_proof
    
    
    def hash(self, block):
        encoded_block = str(block).encode() # Convert block to string and then to bytes
        return hashlib.sha256(encoded_block).hexdigest() # Return the SHA-256 hash of the block
    
    
    def is_chain_valid(self, chain):
        previous_block = chain[0] # Start with the first block
        block_index = 1
        
        while block_index < len(chain):
            block = chain[block_index]
            
            # Check if the previous_hash of the current block matches the hash of the previous block
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            previous_proof = previous_block['proof']
            proof = block['proof']
            # Validate the proof of work
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            
            previous_block = block
            block_index += 1
            
        return True