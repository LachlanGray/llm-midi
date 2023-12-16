import os

test_string = '''\
1-9|4+9|5+9|11/64
4+0|5+0|1/48
4-0|5/64
1+9|4+9|5+8|1/8
0+0|1/64
4+0|1/64
5+0|1/12
9-8|4+8|5+8|3/25
4+0|1/64
5+0|0/1
<EOS>
1-9|4+9|5+9|11/64
4+0|5+0|1/48
4-0|5/64
1+9|4+9|5+8|1/8
0+0|1/64
<EOS>
'''

def write_and_load_consistent():
    from tokenizer import encode
    from train_data import read_data
    import struct

    test_file = './cache/test/testwrite.bin' 

    ids = encode(test_string)
    with open(test_file, 'ab') as f:
        for token_id in ids:
            f.write(struct.pack('h', token_id))

    start, end = 0, 13

    read_ids = read_data(start, end, train_file=test_file)

    for a, b in zip(ids, read_ids):
        print(f"{a}{(8-len(str(a)))*' '}-> {b}")

    assert (ids[start:end] == read_ids).all(), "read/write doesn't match"


def load_data():
    in_file = "./cache/test/train.bin"
    assert os.path.exists(in_file), "No train.bin, do test-write_data first"
    from train_data import read_data
    from tokenizer import decode

    tokens = read_data(0, 1024, train_file=in_file)

    print("READ TOKENS ----------------------------------------")
    for token in tokens:
        print(f"    {token}")

    print(" RESULT ----------------------------------------")
    decoded_tokens = decode(tokens)
    print("".join(list(decoded_tokens)))


def write_data():
    from train_data import make_train_bin

    out_file = "./cache/test/train.bin"

    if os.path.exists(out_file):
        os.remove(out_file)

    # os.(out_file)

    make_train_bin(train_file=out_file, n=30)


def tokenizer():
    from tokenizer import encode, decode


    print(test_string)
    print('------------------------------')
    encoded = encode(test_string)
    print(encoded)
    print('------------------------------')

    decoded = decode(encoded)
    print(decoded)

    assert test_string == decoded

def dataset():
    from dataset import split_dataset
    print(split_dataset)


def debug_event_generation():
    import mido
    from midi_parser import generate_events
    with open("./cache/test/midi_data_index.txt") as f:
        s = f.readlines()[10]
        s = s.strip()

    midi_file = mido.MidiFile(s)

    track = midi_file.tracks[1]
    ticks_per_beat = midi_file.ticks_per_beat

    for event in generate_events(track, ticks_per_beat):
        print(repr(event))

def debug_track():
    import mido
    from midi_parser import Track
    with open("./cache/midi_catalogue.txt") as f:
        s = f.readlines()[10]
        s = s.strip()

    midi_file = mido.MidiFile(s)

    track = midi_file.tracks[1]
    ticks_per_beat = midi_file.ticks_per_beat

    track = Track(track, ticks_per_beat)
    print(track)

def debug_compile_track():
    import mido
    from midi_parser import Track
    with open("./cache/midi_catalogue.txt") as f:
        s = f.readlines()[10]
        s = s.strip()

    midi_file = mido.MidiFile(s)

    track = midi_file.tracks[1]
    ticks_per_beat = midi_file.ticks_per_beat

    track = Track(track, ticks_per_beat)
    print(track.format())

def debug_batch():
    from midi_parser import batch_process
    batch_process()


