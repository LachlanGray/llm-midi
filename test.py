import os


def tokenizer():
    from transformers import PreTrainedTokenizerFast
    tokenizer = PreTrainedTokenizerFast(tokenizer_file='./cache/tokenizer.json')

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
5+0|0/1\
'''

    print(test_string)
    print('------------------------------')
    encoded = tokenizer.encode(test_string)
    print(encoded)
    print('------------------------------')

    decoded = "".join(tokenizer.convert_ids_to_tokens(encoded))
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


