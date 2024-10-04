# Simple Dm-verity Python Implementation

## Overview

This project provides a simplified Python implementation of a dm-verity-like integrity checking system. Dm-verity is a Linux kernel security feature that provides transparent integrity checking of block devices. This implementation demonstrates the core concepts of dm-verity in a easy-to-understand Python script.

## Features

- Block-level integrity checking
- Merkle tree hash generation
- File tampering detection
- Simple API for verifying individual blocks or entire files

## Requirements

- Python 3.6+
- No external dependencies required

## How It Works

1. **Hash Generation**: The file is divided into fixed-size blocks (default 4KB), and a SHA-256 hash is calculated for each block.
2. **Merkle Tree**: A Merkle tree is constructed from these hashes, with the root hash representing the entire file.
3. **Verification**: During verification, each block's hash is recalculated and compared against the stored hash.
4. **Tamper Detection**: Any modification to the file will result in a hash mismatch, indicating tampering.

## Limitations

This is a simplified implementation for educational purposes and lacks many features of a full dm-verity implementation:

- Not integrated with the block device layer
- Does not include cryptographic signing of the root hash
- Not optimized for performance on large files
- Does not handle system reboots or persistent storage of verification state
