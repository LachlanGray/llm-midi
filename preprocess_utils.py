import mido
import os
import re
import math
import json
from fractions import Fraction

def read_index():
    with open('./cache/midi_data_index.txt') as f:
        return [file.strip() for file in f.readlines()]

def get_processed():
    with open('./cache/processed.txt') as f:
        return [file.strip() for file in f.readlines()]

def make_velocity_map():
    if os.path.exists('./cache/velocity_map.json'):
        os.remove('./cache/velocity_map.json')

    base = 9
    mapping = {0:0}

    for i in range(1,128):
        mapping[i] = math.floor(math.log(i, 1.65))

    with open('./cache/velocity_map.json', 'w') as outfile:
        json.dump(mapping, outfile)

if not os.path.exists('./cache/velocity_map.json'):
    make_velocity_map()

# velocity_map = json.loads(f)
with open('./cache/velocity_map.json') as f:
    velocity_map_str = json.load(f)
    velocity_map = {int(k):v for k,v in velocity_map_str.items()}
    del velocity_map_str

def quantize_velocity(velocity):
    return velocity_map[velocity]

def quantize_time(time):
    approx = Fraction(time).limit_denominator(64)
    return approx.numerator, approx.denominator

def find_midi_files(path):
    files = []
    subdirs = []
    for file in os.listdir(path):

        if file.endswith(".mid"):
            files.append(os.path.join(path[11:], file)) # remove ./raw_data/

        if os.path.isdir(os.path.join(path, file)):
            subdirs.append(file)

    for subdir in subdirs:
        found = find_midi_files(os.path.join(path, subdir))
        if found:
            files.extend(found)

    return files

def save_index(path):
    files = find_midi_files(path)

    with open(f'./cache/midi_data_index.txt', 'w') as f:
        for file in files:
            f.write(file.strip() + '\n')


def get_initial_tempo(midi_file) -> int:
    # chooses first tempo message
    for track in midi_file.tracks:
        for message in track:
            if message.type == 'set_tempo':
                return message.tempo


def get_initial_time_scale(midi_file) -> float:
    if midi_file.ticks_per_beat:
        ticks_per_beat = midi_file.ticks_per_beat
    else:
        ticks_per_beat = 480

    try:
        tempo = get_initial_tempo(midi_file) / ticks_per_beat / 1000000
    except:
        tempo = 120 / ticks_per_beat / 1000000

    return tempo



# with open('midi_catalogue.txt', 'r') as f:
#     files = [file.strip() for file in f.readlines()]
# file = files[10]

