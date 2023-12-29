import os
import argparse

"""
Main CLI for the processing etc
"""

from preprocess_utils import save_index
def refresh_index(subparsers):
    parser = subparsers.add_parser('refresh_index', help='Update catalogue')
    parser.add_argument('--data_dir', type=str, default='raw_data', help='data directory')
    parser.add_argument('--overwrite', action='store_true', help='overwrite existing files')

    parser.set_defaults(func=main_refresh_index)

def main_refresh_index(args):
    # index_patph = os.path.join(args.data_dir, 'catalogue')

    if os.path.exists('./cache/midi_data_index.txt') and not args.overwrite:
        print('Index already exists')
        return

    save_index('./raw_data')


from midi_parser import batch_process
from preprocess_utils import read_index, get_processed
def make_dataset(subparsers):
    parser = subparsers.add_parser('make_dataset', help='Make text dataset from midi dir')
    # parser.add_argument('-n', type=int, default=1000, help='Number of files to process')
    parser.add_argument('--limit', type=int, default=None, help='Specify a number of files to process')

    parser.set_defaults(func=main_make_dataset)

def main_make_dataset(args):
    files = set(read_index())
    processed = set(get_processed())
    files = files - processed

    limit = args.limit

    batch_process(list(files)[:limit])


from tokenizers import Tokenizer as TokenizerFast
from tokenizers.models import BPE

def make_tokenizer(subparsers):
    parser = subparsers.add_parser('make_tokenizer', help='Make text dataset from midi dir')

    parser.set_defaults(func=main_make_tokenizer)

class FileIterator:
    def __init__(self, dataset_dir='./data'):
        self.dataset_dir = dataset_dir

    def __iter__(self):
        data_dir = './data/'
        files = os.listdir(data_dir)
        for file in files:
            with open(os.path.join(data_dir, file), 'r') as f:
                lines = f.readlines()
                if lines == []:
                    continue

                yield lines


def main_make_tokenizer(args):

    bpe_model = TokenizerFast(
        BPE(
            # vocab=None,
            # merges=[],
            vocab_size=300,
            dropout=None,
            continuing_subword_prefix="",
            end_of_word_suffix="",
            fuse_unk=False,
        )
    )

    files = FileIterator() # skips empty files

    bpe_model.train_from_iterator(files)
    bpe_model.save('./cache/tokenizer.json')


def make_train_bin(subparsers):
    parser = subparsers.add_parser('make_train_bin', help='Make train bin')

    parser.set_defaults(func=main_make_train_bin)

def main_make_train_bin(args):
    from train_data import make_train_bin

    make_train_bin()



# Example usage
if __name__ == "__main__":
    main_parser = argparse.ArgumentParser(description='Main parser')
    subparsers = main_parser.add_subparsers(help='sub-command help')

    # Add subparsers here
    refresh_index(subparsers)
    make_dataset(subparsers)
    make_tokenizer(subparsers)
    make_train_bin(subparsers)

    args = main_parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        main_parser.print_help()

