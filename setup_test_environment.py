#!/usr/bin/env python3
"""
Helper script to create a test environment with sample files.
"""

import os
import random
from pathlib import Path


def create_test_directory():
    """Create the crypto_benchmark_test directory with sample files."""
    test_dir = Path("crypto_benchmark_test")
    test_dir.mkdir(exist_ok=True)
    
    print(f"📁 Creating test directory: {test_dir.resolve()}")
    
    # Create files of various sizes
    test_files = [
        ("small_file.txt", 1024),           # 1 KB
        ("medium_file.txt", 1024 * 100),    # 100 KB
        ("large_file.txt", 1024 * 1024),    # 1 MB
        ("binary_data.bin", 1024 * 512),    # 512 KB
    ]
    
    for filename, size in test_files:
        filepath = test_dir / filename
        
        # Generate random data
        data = bytes(random.randint(0, 255) for _ in range(size))
        
        with open(filepath, 'wb') as f:
            f.write(data)
        
        print(f"   ✓ Created {filename} ({size:,} bytes)")
    
    print(f"\n✅ Test environment ready!")
    print(f"   Run: python crypto_benchmark.py crypto_benchmark_test")


if __name__ == "__main__":
    create_test_directory()
