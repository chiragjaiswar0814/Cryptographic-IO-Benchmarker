#!/usr/bin/env python3
"""
Cryptography I/O Benchmark Tool
Tests AES-256 encryption performance on local storage using Fernet (AES-128-CBC with HMAC).
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple
from cryptography.fernet import Fernet


class CryptoBenchmark:
    """Benchmark tool for testing encryption/decryption I/O performance."""
    
    REQUIRED_FOLDER_NAME = "crypto_benchmark_test"
    
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir).resolve()
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.results: Dict[str, float] = {}
        
    def validate_directory(self) -> bool:
        """Safety check: only run if folder is named /crypto_benchmark_test/"""
        if self.target_dir.name != self.REQUIRED_FOLDER_NAME:
            print(f"❌ SAFETY CHECK FAILED!")
            print(f"   Target directory must be named '{self.REQUIRED_FOLDER_NAME}'")
            print(f"   Got: {self.target_dir.name}")
            return False
            
        if not self.target_dir.exists():
            print(f"❌ Directory does not exist: {self.target_dir}")
            return False
            
        if not self.target_dir.is_dir():
            print(f"❌ Path is not a directory: {self.target_dir}")
            return False
            
        return True
    
    def get_files(self) -> List[Path]:
        """Get all files in the target directory (non-recursive)."""
        files = [f for f in self.target_dir.iterdir() if f.is_file()]
        return files
    
    def encrypt_files(self, files: List[Path]) -> Tuple[float, int]:
        """
        Encrypt all files in place.
        Returns: (elapsed_time, total_bytes_processed)
        """
        total_bytes = 0
        start_time = time.perf_counter()
        
        for file_path in files:
            # Read original file
            with open(file_path, 'rb') as f:
                plaintext = f.read()
            
            total_bytes += len(plaintext)
            
            # Encrypt
            ciphertext = self.cipher.encrypt(plaintext)
            
            # Write encrypted data back
            with open(file_path, 'wb') as f:
                f.write(ciphertext)
        
        elapsed = time.perf_counter() - start_time
        return elapsed, total_bytes
    
    def decrypt_files(self, files: List[Path]) -> Tuple[float, int]:
        """
        Decrypt all files in place.
        Returns: (elapsed_time, total_bytes_processed)
        """
        total_bytes = 0
        start_time = time.perf_counter()
        
        for file_path in files:
            # Read encrypted file
            with open(file_path, 'rb') as f:
                ciphertext = f.read()
            
            # Decrypt
            plaintext = self.cipher.decrypt(ciphertext)
            
            total_bytes += len(plaintext)
            
            # Write decrypted data back
            with open(file_path, 'wb') as f:
                f.write(plaintext)
        
        elapsed = time.perf_counter() - start_time
        return elapsed, total_bytes
    
    def format_bytes(self, bytes_count: int) -> str:
        """Format bytes into human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_count < 1024.0:
                return f"{bytes_count:.2f} {unit}"
            bytes_count /= 1024.0
        return f"{bytes_count:.2f} TB"
    
    def format_throughput(self, bytes_count: int, seconds: float) -> str:
        """Calculate and format throughput."""
        if seconds == 0:
            return "N/A"
        throughput = bytes_count / seconds
        return f"{self.format_bytes(throughput)}/s"
    
    def print_report(self, file_count: int, encrypt_time: float, decrypt_time: float, 
                     encrypt_bytes: int, decrypt_bytes: int):
        """Print performance report."""
        print("\n" + "="*60)
        print("CRYPTOGRAPHY I/O BENCHMARK REPORT")
        print("="*60)
        print(f"\n📁 Target Directory: {self.target_dir}")
        print(f"📄 Files Processed:  {file_count}")
        print(f"💾 Total Data Size:  {self.format_bytes(encrypt_bytes)}")
        print(f"🔑 Cipher:           Fernet (AES-128-CBC + HMAC-SHA256)")
        
        print(f"\n{'─'*60}")
        print("ENCRYPTION PHASE")
        print(f"{'─'*60}")
        print(f"⏱️  Time Elapsed:    {encrypt_time:.4f} seconds")
        print(f"⚡ Throughput:       {self.format_throughput(encrypt_bytes, encrypt_time)}")
        
        print(f"\n{'─'*60}")
        print("DECRYPTION PHASE")
        print(f"{'─'*60}")
        print(f"⏱️  Time Elapsed:    {decrypt_time:.4f} seconds")
        print(f"⚡ Throughput:       {self.format_throughput(decrypt_bytes, decrypt_time)}")
        
        print(f"\n{'─'*60}")
        print("SUMMARY")
        print(f"{'─'*60}")
        total_time = encrypt_time + decrypt_time
        print(f"⏱️  Total Time:      {total_time:.4f} seconds")
        print(f"📊 Avg Throughput:  {self.format_throughput(encrypt_bytes + decrypt_bytes, total_time)}")
        
        if encrypt_time > 0 and decrypt_time > 0:
            ratio = decrypt_time / encrypt_time
            print(f"🔄 Decrypt/Encrypt: {ratio:.2f}x")
        
        print("="*60 + "\n")
    
    def run(self):
        """Execute the benchmark."""
        print("\n🔐 Cryptography I/O Benchmark Tool")
        print("="*60)
        
        # Safety validation
        if not self.validate_directory():
            sys.exit(1)
        
        # Get files
        files = self.get_files()
        if not files:
            print(f"⚠️  No files found in {self.target_dir}")
            sys.exit(0)
        
        print(f"✅ Safety check passed")
        print(f"📂 Found {len(files)} file(s) to process")
        
        # Confirm operation
        print(f"\n⚠️  WARNING: Files will be encrypted and then decrypted in place!")
        response = input("Continue? (yes/no): ").strip().lower()
        if response != 'yes':
            print("❌ Benchmark cancelled")
            sys.exit(0)
        
        print("\n🔄 Starting benchmark...\n")
        
        # Encryption phase
        print("🔒 Encrypting files...")
        encrypt_time, encrypt_bytes = self.encrypt_files(files)
        print(f"   ✓ Encrypted {len(files)} file(s) in {encrypt_time:.4f}s")
        
        # Decryption phase
        print("🔓 Decrypting files...")
        decrypt_time, decrypt_bytes = self.decrypt_files(files)
        print(f"   ✓ Decrypted {len(files)} file(s) in {decrypt_time:.4f}s")
        
        # Generate report
        self.print_report(len(files), encrypt_time, decrypt_time, 
                         encrypt_bytes, decrypt_bytes)


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python crypto_benchmark.py <target_directory>")
        print(f"\nNote: Target directory must be named 'crypto_benchmark_test' for safety")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    benchmark = CryptoBenchmark(target_dir)
    benchmark.run()


if __name__ == "__main__":
    main()
