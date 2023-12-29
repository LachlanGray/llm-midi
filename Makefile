
.PHONY: clean index dataset tokenizer test-% delete-training-data 

index:
	# creates the index
	python main.py refresh_index

dataset:
	# populate ./data n midi files at a time
	python main.py make_dataset

tokenizer:
	# trains a tokenizer on every file in ./data/
	python main.py make_tokenizer

train-bin:
	# tokenize every file in ./data, and concatenate into ./train/train.bin
	python main.py make_train_bin

test-%:
	python -c "from test import $*; $*()"

delete-training-data:
	rm ./cache/processed.txt
	rm ./data/*
	rm ./train.bin

