import datasets
from transformers import PreTrainedTokenizerFast

import os
import random
import numpy as np
from tqdm import tqdm

random.seed(1)
num_proc=4

train_test_split = 0.0005
files = os.listdir('./data/')
random.shuffle(files)

split_index = int(len(files) * train_test_split)
n_train = len(files) - split_index
n_test = split_index

def file_generator(shards):
    if set == 'train':
        files = files[split_index:]
    else:
        files = files[:split_index]

    for shard in shards:
        with open(shard) as f:
            for file in files:
                with open(f'./data/{file}', 'r') as f:
                    yield {"text": f.read()}

# TODO: tokenze dataset

train_dataset = datasets.IterableDataset.from_generator(file_generator)
# test_dataset = datasets.IterableDataset.from_generator(file_generator)

tokenizer = PreTrainedTokenizerFast(tokenizer_file='./cache/tokenizer.json')

def process(example):
    ids = tokenizer.encode(example['text'], add_special_tokens=False)
    ids.append(tokenizer.eos_token_id)
    return {"ids": ids, "len": len(ids)}

tokenized = train_dataset.map(
    process,
    remove_columns=['text'],
)


# THEN this


total_batches = 1024
arr_len = np.sum(n_train, dtype=np.uint64)
filename = "train.bin"
dtype = np.uint16 # (can do since enc.max_token_value == 50256 is < 2**16)
arr = np.memmap(filename, dtype=dtype, mode='w+', shape=(arr_len,))

idx = 0
for batch_idx in tqdm(range(total_batches)):
    batch = train_dataset.shard(num_shards=total_batches, desc='writing test.bin')
    arr_batch = np.concatenate(batch['ids'])

    arr[idx: idx + len(arr_batch)] = arr_batch

    idx += len(arr_batch)

arr.flush()



