## Setup
Dump a whole bunch of midi files into `/raw_data` in the project root. They can be inside nested folders. Make an index of all the files with
```
make index  
```

Then, to convert the midi files to a llm-friendly format do
```
make dataset
```
This will convert all the indexed midi files to a text format and store them as flat files in `./data`. One file is created for each track in a midi file.

Once that's done, you can train a tokenizer on the files in `./data` with
```
make tokenizer
```
which will create `./cache/tokenizer.json`. Finally, you can initialize the actual training binary with 
```
make train-bin
```
which will create `train.bin`



***
Parse N midi files into text, and save to `./data`. I'm doing it like this right now because this part can be slow and interupting it will mess it up. The translated files will appear as `./data/file_n.txt` where `file` is the name of the midi file (excluding parent folders), and `n` is the track number from the file.
```
make dataset-N
```

A sequence of tokens can be read over one interval with `train_data.read_data(start, end)`. 


Train the tokenizer on the translated files. It will train on all the files, should be fast.
```
make tokenizer
```

Assemble the translated text representations into a `train.bin`. It is located in `./train`, and each token is stored as 2 bytes.
```
make train-bin
```


## Tests
```
make test-name_of_test
```
where `name_of_test` is a function in `test.py`


## What is this
I want to use language models to compose music by having them "speak" the [midi protocol](https://en.wikipedia.org/wiki/MIDI). This is how projects like [MuseNet](https://openai.com/research/musenet) work. Alas generative music still sounds really weird to me.

Music is a language, so it's weird that language models don't seem to do it well. Lack of training data is probably a big reason, but I also think a problem is that language models are not good at math and counting.

The way we record and formalize music looks a lot more like math than language. When we describe music in western notation, we describe a melody in terms of the specific notes that are played, and their specific durations in terms of beats. But when most people *hear* music, the percieved semantics aren't encoded in the absolute frequency of individual notes, but their *relative* frequencies and durations. It's way easier to develop relative pitch than perfect pitch.

So something that I think might be neat is to describe the music in relative terms instead of absolute terms. For example, ignoring octaves, there are 12 different major triads you can play, `(C,E,G)`, `(C#, F, G#)`, ..., `(B,Eb,Gb)`. To most people though, there isn't a meaningful difference between, e.g., C major and C# major, unless they are heard together. So instead of describing a chord by those names, it might be easier to describe them just as "major triad", and let the exact chord be decided by the starting note.


## So Far...
The encoding is broken into newline-separated events. The contents of one line are simultaneous, and separated by vertical bars. One event contains one or more (interval, sign, velocity) triplets, and closes with a duration.
```
(interval)(sign)(velocity)|...|(count)/(unit)
```

The interval is a number of piano keys, the sign is whether to go up or down by that much, and the velocity is how loud to play it at. 

The time duration at the end can be any fraction of a beat.

For now a bunch of information is discarded, like tempo, instrument, sustain, ... . When you train a foundation language model, you don't have to label the examples by mood or style for the langauge model to capture those qualities. In a similar way, I think there is enough information in a melody to infer qualities like tempo and instrument, and complete the sequence appropriately.

As a language, music's "grammar" is much less specific than spoken language, and it feels like small models should go a long way.

Next step is to train something.


