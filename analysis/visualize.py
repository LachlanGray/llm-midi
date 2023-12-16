import matplotlib.pyplot as plt
import mido
import os
from ..preprocess_utils import get_initial_time_scale, get_initial_tempo

def plot_timescale():

    if os.path.exists('time_scales.txt'):
        with open('time_scales.txt', 'r') as f:
            time_scales = [float(scale.strip()) for scale in f.readlines()]
        plt.hist(time_scales, bins=1000)
        plt.title('Initial Time Scales')
        # limit to 0.1
        # plt.gca().set_xlim([0, 0.04])
        # log axis
        # plt.gca().set_yscale("log")
        plt.show()
        return

    with open('midi_catalogue.txt', 'r') as f:
        files = [file.strip() for file in f.readlines()]

    print(files[0])
    total = len(files)
    done = 0

    failed_files = []

    time_scales = []
    for file in files[:5000]:
        print("\033c")
        print(f"{done}/{total}")
        try:
            midi_file = mido.MidiFile(file)
        except:
            failed_files.append(file)
            continue

        time_scale = get_initial_time_scale(midi_file)
        del midi_file

        time_scales.append(time_scale)
        done += 1

    plt.hist(time_scales, bins=100)
    plt.title('Initial Time Scales')
    plt.show()

    with open('time_scales.txt', 'w') as f:
        for time_scale in time_scales:
            f.write(str(time_scale) + '\n')

    with open('corrupt.txt', 'w') as f:
        for file in failed_files:
            f.write(file + '\n')

def plot_tempos():
    import matplotlib.pyplot as plt

    N = 500

    if os.path.exists(f'cache/tempos/tempos_{N}.txt'):
        with open(f'cache/tempos/tempos_{N}.txt', 'r') as f:
            tempos = [float(tempo.strip()) for tempo in f.readlines()]

        plt.hist(tempos, bins=100)
        plt.title('Initial Tempos')
        plt.show()


    with open('midi_catalogue.txt', 'r') as f:
        files = [file.strip() for file in f.readlines()]

    total = len(files)
    done = 0

    failed_files = []

    tempos = []
    for file in files[:N]:
        print("\033c")
        print(f"{done}/{total}")
        try:
            midi_file = mido.MidiFile(file)
        except:
            failed_files.append(file)
            continue

        tempo = get_initial_tempo(midi_file)
        del midi_file

        tempo = 1 / ( tempo / 1000000 / 60 )
        tempos.append(tempo)
        done += 1

    with open(f'cache/tempos/tempos_{N}.txt', 'w') as f:
        for tempo in tempos:
            f.write(str(tempo) + '\n')

    plt.hist(tempos, bins=100)
    plt.title('Initial Tempos')
    plt.show()


plot_tempos()
