# Cryptography I/O Benchmark Tool

A Python-based benchmark tool to test the I/O bottleneck of AES encryption on local storage using the `cryptography.fernet` library.

## Features

- ✅ **Safety First**: Hardcoded check ensures the tool only runs on directories named `crypto_benchmark_test`
- 🔐 **Fernet Encryption**: Uses Fernet (AES-128-CBC with HMAC-SHA256) from the cryptography library
- ⚡ **Performance Metrics**: Measures encryption and decryption throughput
- 📊 **Detailed Reports**: Provides comprehensive timing and throughput statistics
- 🔄 **Reversible**: Encrypts files then immediately decrypts them back to original state

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

1. Create a test environment with sample files:
```bash
python setup_test_environment.py
```

2. Run the benchmark:
```bash
python crypto_benchmark.py crypto_benchmark_test
```

### Manual Setup

1. Create a directory named `crypto_benchmark_test`:
```bash
mkdir crypto_benchmark_test
```

2. Add files to benchmark (any files you want to test)

3. Run the benchmark:
```bash
python crypto_benchmark.py crypto_benchmark_test
```

## Safety Features

The script includes a **mandatory safety check**:
- ❌ Will **refuse to run** unless the target directory is named exactly `crypto_benchmark_test`
- ⚠️ Prompts for confirmation before modifying files
- 🔒 Uses in-memory key generation (files are restored to original state)

## Example Output

```
🔐 Cryptography I/O Benchmark Tool
============================================================
✅ Safety check passed
📂 Found 4 file(s) to process

⚠️  WARNING: Files will be encrypted and then decrypted in place!
Continue? (yes/no): yes

🔄 Starting benchmark...

🔒 Encrypting files...
   ✓ Encrypted 4 file(s) in 0.0234s
🔓 Decrypting files...
   ✓ Decrypted 4 file(s) in 0.0198s

============================================================
CRYPTOGRAPHY I/O BENCHMARK REPORT
============================================================

📁 Target Directory: /path/to/crypto_benchmark_test
📄 Files Processed:  4
💾 Total Data Size:  1.62 MB
🔑 Cipher:           Fernet (AES-128-CBC + HMAC-SHA256)

────────────────────────────────────────────────────────────
ENCRYPTION PHASE
────────────────────────────────────────────────────────────
⏱️  Time Elapsed:    0.0234 seconds
⚡ Throughput:       69.23 MB/s

────────────────────────────────────────────────────────────
DECRYPTION PHASE
────────────────────────────────────────────────────────────
⏱️  Time Elapsed:    0.0198 seconds
⚡ Throughput:       81.82 MB/s

────────────────────────────────────────────────────────────
SUMMARY
────────────────────────────────────────────────────────────
⏱️  Total Time:      0.0432 seconds
📊 Avg Throughput:  75.00 MB/s
🔄 Decrypt/Encrypt: 0.85x

============================================================
```

## Technical Details

### Encryption Algorithm
- **Library**: `cryptography.fernet`
- **Cipher**: AES-128-CBC with HMAC-SHA256
- **Key Size**: 256-bit (URL-safe base64-encoded)
- **Authentication**: Built-in HMAC for integrity verification

### Benchmark Process
1. Validates target directory name matches `crypto_benchmark_test`
2. Generates a random Fernet key
3. Reads each file's bytes into memory
4. Encrypts the data and writes back to disk
5. Times the encryption operation
6. Immediately decrypts all files back to original state
7. Times the decryption operation
8. Generates performance report with throughput metrics

### Limitations
- Files are processed sequentially (not parallelized)
- Entire file contents are loaded into memory
- Only processes files in the target directory (non-recursive)
- Fernet uses AES-128-CBC, not AES-256 (Fernet specification)

## Note on AES-256

While the project brief mentions AES-256, the `cryptography.fernet` library uses **AES-128-CBC** as specified by the Fernet format. Fernet provides:
- AES-128 encryption in CBC mode
- HMAC-SHA256 for authentication
- Timestamp for expiration support
- URL-safe base64 encoding

If you specifically need AES-256, you would need to use `cryptography.hazmat.primitives.ciphers` directly instead of Fernet.

## License

This is a benchmark tool for testing purposes.
