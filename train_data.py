import os
from tokenizer import encode
import struct
import numpy as np
from tqdm import tqdm


""" Another way of memory mapping
import mmap
import os

# Step 1: Create a file
file_path = "example.dat"
with open(file_path, "wb") as f:
    f.write(b'\x00' * 1024)  # Write 1024 null bytes as placeholder

# Step 2: Memory map the file
with open(file_path, "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)

    # Step 3: Write to the memory-mapped file
    mm[0:11] = b'Hello World'

    # Read from the memory-mapped file
    print(mm[:11])  # Output: b'Hello World'

    # Step 5: Close the memory map and the file
    mm.close()

"""

TRAIN_DIR = './train'
TRAIN_FILE = os.path.join(TRAIN_DIR, 'train.bin')
DATA_DIR = './data'

if not os.path.exists('./train'):
    os.mkdir('./train/')

if os.path.exists(DATA_DIR):
    train_files = os.listdir(DATA_DIR)
    assert len(train_files) > 0, f"No training files in {DATA_DIR}"
else:
    assert False, f"Directory {DATA_DIR} does not exist"

def make_train_bin(train_file=TRAIN_FILE, n=None):
    for file in tqdm(train_files[:n], "Making train.bin"):
        with open(os.path.join(DATA_DIR, file), 'r') as f:
            data = f.read()

        if data == "":
            continue

        data += '<EOS>\n'

        ids = encode(data)

        with open(train_file, 'ab') as f:
            for token_id in ids:
                f.write(struct.pack('h', token_id))

def read_data(start_idx: int, length: int, train_file=TRAIN_FILE)-> np.ndarray:
    with open(train_file, 'rb') as f:

        f.seek(start_idx * 2) # each token is 2 bytes
        sequence = np.fromfile(
            f,
            dtype=np.int16,
            count=length
        )

        return sequence



