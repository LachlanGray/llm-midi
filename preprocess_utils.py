import mido
import os
import re
import math
import json
from fractions import Fraction

"""
Methods for extracting/calculating relevant information from midi files
"""

def read_index():
    """
    return list of paths to all midi files in ./raw_data
    """
    with open('./cache/midi_data_index.txt') as f:
        return [file.strip() for file in f.readlines()]

def get_processed():
    """
    return list of converted text files stored in ./data
    """
    try:
        with open('./cache/processed.txt') as f:
            return [file.strip() for file in f.readlines()]
    except:
        print("cache/processed.txt doesn't exist")
        return []

def make_velocity_map():
    """
    Create file ./cache/velocity_map.json, used to quantize note velocities
    """
    if os.path.exists('./cache/velocity_map.json'):
        os.remove('./cache/velocity_map.json')

    mapping = {0:0}

    for i in range(1,128):
        mapping[i] = math.floor(math.log(i, 1.65))

    with open('./cache/velocity_map.json', 'w') as outfile:
        json.dump(mapping, outfile)

if not os.path.exists('./cache/velocity_map.json'):
    make_velocity_map()

# load velocity map
with open('./cache/velocity_map.json') as f:
    velocity_map_str = json.load(f)
    velocity_map = {int(k):v for k,v in velocity_map_str.items()}
    del velocity_map_str

def quantize_velocity(velocity: int) -> int:
    '''
    quantize midi velocities like [0,127] -> [0,9]
    '''
    return velocity_map[velocity]

def quantize_time(time: float):
    '''
    Takes a time in units of beats, and rounds to the nearest
    fraction
    '''
    approx = Fraction(time).limit_denominator(64)
    return approx.numerator, approx.denominator

def find_midi_files(path):
    '''
    find all midi files in specified path
    '''
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
    """
    index all the midi files in a path, and cache it
    """
    files = find_midi_files(path)

    with open(f'./cache/midi_data_index.txt', 'w') as f:
        for file in files:
            f.write(file.strip() + '\n')


def get_initial_tempo(midi_file) -> int:
    '''
    dumb method to find initial tempo; iterates over messages until a set
    tempo message occurs.

    used to calculate time units
    '''
    for track in midi_file.tracks:
        for message in track:
            if message.type == 'set_tempo':
                return message.tempo


def get_initial_time_scale(midi_file: mido.MidiFile) -> float:
    """
    get the tempo of a  midi file in units of microseconds per beat

    not used for now as we are ignoring tempo; will be useful later
    for tempo tokens.
    """
    if midi_file.ticks_per_beat:
        ticks_per_beat = midi_file.ticks_per_beat
    else:
        ticks_per_beat = 480

    try:
        tempo = get_initial_tempo(midi_file) / ticks_per_beat / 1000000
    except:
        # default tempo of 120
        tempo = 120 / ticks_per_beat / 1000000

    return tempo



# with open('midi_catalogue.txt', 'r') as f:
#     files = [file.strip() for file in f.readlines()]
# file = files[10]

