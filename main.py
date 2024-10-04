import hashlib
import os
import math

class SimpleVerity:
    def __init__(self, data_file, hash_file, block_size=4096):
        # Initialize with the data file to protect, the file to store hashes,
        # and the block size (default 4KB, typical for dm-verity)
        self.data_file = data_file
        self.hash_file = hash_file
        self.block_size = block_size
        self.root_hash = None

    def generate_hashes(self):
        # Generate hashes for each block of the data file
        hashes = []
        with open(self.data_file, 'rb') as f:
            while True:
                block = f.read(self.block_size)
                if not block:
                    break
                # Calculate SHA-256 hash for each block
                block_hash = hashlib.sha256(block).hexdigest()
                hashes.append(block_hash)
        
        # Build the Merkle tree and get the root hash
        self.root_hash = self._build_merkle_tree(hashes)
        return hashes

    def _build_merkle_tree(self, hashes):
        # Build a Merkle tree from the list of hashes
        while len(hashes) > 1:
            new_level = []
            for i in range(0, len(hashes), 2):
                left = hashes[i]
                # If there's an odd number of hashes, duplicate the last one
                right = hashes[i+1] if i+1 < len(hashes) else left
                combined = left + right
                # Calculate the hash of the combined hashes
                new_hash = hashlib.sha256(combined.encode()).hexdigest()
                new_level.append(new_hash)
            hashes = new_level
        # The last remaining hash is the root hash
        return hashes[0]

    def save_hashes(self, hashes):
        # Save the list of hashes to a file
        with open(self.hash_file, 'w') as f:
            for h in hashes:
                f.write(h + '\n')

    def verify_block(self, block_number):
        # Verify a specific block against its stored hash
        with open(self.data_file, 'rb') as f:
            f.seek(block_number * self.block_size)
            block = f.read(self.block_size)
        
        # Calculate the hash of the current block data
        block_hash = hashlib.sha256(block).hexdigest()
        
        # Read the stored hash for this block
        with open(self.hash_file, 'r') as f:
            stored_hashes = f.readlines()
        
        # Compare the calculated hash with the stored hash
        if block_hash == stored_hashes[block_number].strip():
            return True
        return False

    def verify_all_blocks(self):
        # Verify all blocks in the data file
        with open(self.data_file, 'rb') as f:
            # Calculate the total number of blocks, rounding up for partial blocks
            block_count = math.ceil(os.path.getsize(self.data_file) / self.block_size)
        
        for i in range(block_count):
            if not self.verify_block(i):
                print(f"Block {i} verification failed!")
                return False
        
        print("All blocks verified successfully!")
        return True

# Example usage
if __name__ == "__main__":
    # Create a sample data file with 1MB of random data
    with open("sample_data.bin", "wb") as f:
        f.write(os.urandom(1024 * 1024))

    # Initialize the SimpleVerity object
    verity = SimpleVerity("sample_data.bin", "hash_tree.txt")
    
    # Generate hashes for all blocks and save them
    hashes = verity.generate_hashes()
    verity.save_hashes(hashes)
    print(f"Root hash: {verity.root_hash}")

    # Verify all blocks initially
    verity.verify_all_blocks()

    # Verify block 0 specifically before tampering
    print(f"Block 0 verification before tampering: {verity.verify_block(0)}")

    # Simulate tampering by modifying a small portion of the first block
    with open("sample_data.bin", "r+b") as f:
        f.seek(1024)  # This is still within the first block (0-4095 bytes)
        f.write(b"TAMPERED")

    # Verify all blocks again after tampering
    verity.verify_all_blocks()

    # Verify block 0 specifically after tampering
    print(f"Block 0 verification after tampering: {verity.verify_block(0)}")
    print(f"Block 1 verification after tampering: {verity.verify_block(1)}")
