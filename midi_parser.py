import mido
import os
import hashlib
import json
from tqdm import tqdm
# from calculate_bins import quantize_time, quantize_velocity

"""
Methods for translating raw midi files to a text-based format

batch_process() takes a list of midi file paths, translates them,
and writes them to ./data/

It also caches which files have been processed in ./cache/processed.txt

"""

from preprocess_utils import quantize_time, quantize_velocity

def format_note(note: tuple):
    interval = note[0]
    sign = "-" if interval <0 else "+"
    interval = abs(interval)
    velocity = quantize_velocity(note[1])

    return f"{interval}{sign}{velocity}|"

def format_time(time: float):
    num, denom = quantize_time(time)
    return f"{num}/{denom}\n"

class MidiEvent:
    def __init__(self, start_time):
        self.notes = {}
        self.messages = {}
        self.start_time = start_time
        self.duration = 0
        self.root_interval = None
        self.chord_intervals = []


    def format(self):
        if self.root_interval:
            root = format_note(self.root_interval)
            chord_intervals = "".join([format_note(interval) for interval in self.chord_intervals])
            duration = format_time(self.duration)

            return root + chord_intervals + duration

        else:
            return ""


    def __repr__(self):
        return f'<MidiEvent: notes={self.notes}, msgs={self.messages}, time={self.duration:.3f}, abs_time={self.start_time:.3f}>'

    def __str__(self):
        # TODO: replace with token representation
        # return f'<MidiEvent: {self.notes}, {self.messages}, time={self.duration:.3f}, abs_time={self.start_time:.3f}>'
        if self.root_interval:
            chord_tones = ", ".join([f"{t[0]}:{t[1]}" for t in self.chord_intervals])
            duration = f'{self.duration:.3f}'

            left = f'{self.root_interval[0]}:{self.root_interval[1]}'
            pad = " "*(8 - len(left))
            return f"{duration} | {left}{pad} | {chord_tones}"
        else:
            return f'{self.messages} '


def generate_events(track, ticks_per_beat):
    current_time = 0
    current_event = MidiEvent(current_time)
    tempo_changes = {}

    beats_per_tick = 1./ticks_per_beat # convert units of time to beats
    mins_per_microsecond = 1.6666666e-8

    for message in track:

        beats_since_last = message.time * beats_per_tick

        if beats_since_last > 0:
            current_event.duration = beats_since_last
            # current_event.notes = sorted(current_event.notes) # organize chords low -> high
            # current_event.notes = {note: velocity for note, velocity in sorted(current_event.notes.items())}
            # sorted(current_event.notes)

            yield current_event
            current_time += beats_since_last
            current_event = MidiEvent(current_time)

        if message.type == 'note_on':
            note, velocity = message.bytes()[1:]
            current_event.notes[note] = velocity
        elif message.type == 'note_off':
            note = message.bytes()[1]
            current_event.notes[note] = 0
        elif message.type == 'control_change':
            if message.control == 64: # sustain pedal
                current_event.messages['sustain'] = message.bytes()[-1]
        elif message.type == 'set_tempo':
            tempo_bpm = 1. / (message.tempo * mins_per_microsecond)
            current_event.messages['set_tempo'] = tempo_bpm
            tempo_changes[current_time] = tempo_bpm
        elif message.type == 'end_of_track':
            current_event.messages['end_of_track'] = True
            current_event.messages['all_tempo_changes'] = tempo_changes
            yield current_event
            return
        else:
            continue


class Track:
    def __init__(self, track, ticks_per_beat):
        # TODO: handle velocity = 0, make note stack?k
        root_note = 60
        self.events = []
        self.is_empty = False

        for event in generate_events(track, ticks_per_beat):

            if event.notes:
                notes = sorted(list(event.notes.items()))
                new_root_note, root_velocity = notes[0]
                root_interval = new_root_note - root_note
                root_note = new_root_note

                if len(notes) > 1:
                    chord_intervals = []
                    prev_tone = root_note

                    for note in notes[1:]:
                        tone, velocity = note
                        tone_interval = tone - prev_tone
                        prev_tone = tone

                        chord_intervals.append((tone_interval, velocity))

                    event.chord_intervals = chord_intervals

                event.root_interval = (root_interval, root_velocity)

            self.events.append(event)

        tempo_changes = self.events[-1].messages['all_tempo_changes']

        self.tempo_changes = tempo_changes

    def __str__(self):
        return "\n".join([str(event) for event in self.events])

    def format(self):
        return "".join([event.format() for event in self.events])

def process_midi_file(path: str):
    try:
        file = mido.MidiFile(path)
    except:
        yield None
        return

    ticks_per_beat = file.ticks_per_beat
    tracks = file.tracks

    for track in tracks:
        parsed = Track(track, ticks_per_beat)
        yield parsed


def batch_process(files: list[str]):
    '''
    files: list of paths inside ./raw_data of midi files

    '''
    cache_file = './cache/processed.txt'

    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            processed_files = set(json.loads(f.read()))
    else:
        processed_files = set()

    # wrapped in try/except so that if you <C-c>, progress is stored
    try:
        for file in tqdm(files, "processing files"):
            if file in processed_files:
                continue

            try:
                for n, track in enumerate(process_midi_file("./raw_data/" + file)):
                    if track:
                        name = f"./data/{file.split('/')[-1]}_{n}.txt"

                        with open(name, "w") as f:
                            f.write(track.format())
                    else:
                        continue
            except:
                with open('./cache/failed.txt', 'a') as f:
                    f.write(file + '\n')


            processed_files.add(file)
    except:
        processed_files.add(file)

    with open(cache_file, 'w') as f:
        f.write(json.dumps(list(processed_files)))



