#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime

HEADER_BYTES = 64  # 512 bits

def freeze_file(input_path, output_path=None):
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    with open(input_path, "rb") as f:
        data = f.read()

    header = data[:HEADER_BYTES]
    sha512_hash = hashlib.sha512(data).hexdigest()

    stat = os.stat(input_path)

    metadata = {
        "icecofin_version": "1.0",
        "original_filename": os.path.basename(input_path),
        "original_size_bytes": len(data),
        "file_extension": os.path.splitext(input_path)[1],
        "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "header_512_bits_hex": header.hex(),
        "sha512_hash_hex": sha512_hash,
        "note": "Decompression scheduled for 10^24 years in the future."
    }

    if output_path is None:
        output_path = input_path + ".icecofin"

    with open(output_path, "w") as out:
        json.dump(metadata, out, indent=4)

    print(f"Frozen → {output_path}")
    print("Decompression unavailable until year ~10^24.")

def main():
    parser = argparse.ArgumentParser(
        description="ICE COFIN — Irreversible Compression Engine"
    )
    parser.add_argument("input", help="File to freeze")
    parser.add_argument("-o", "--output", help="Output .icecofin file")

    args = parser.parse_args()

    try:
        freeze_file(args.input, args.output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
