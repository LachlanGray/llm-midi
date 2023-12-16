
.PHONY: clean catalogue dataset tokenizer test-% delete-training-data

index:
	python main.py refresh_index

dataset: catalogue
	python main.py make_dataset

tokenizer:
	# trains a tokenizer on every file in ./data/
	python main.py make_tokenizer

test-%:
	python -c "from test import $*; $*()"
	

delete-training-data:
	rm ./cache/processed.txt
	rm ./data/*

