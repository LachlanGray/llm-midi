from transformers import PreTrainedTokenizerFast


tokenizer = PreTrainedTokenizerFast(
    tokenizer_file='./cache/tokenizer.json',
    eos_token='<EOS>')

def encode(s: str) -> list[int]:
    return tokenizer.encode(s)

def decode(ids: list[int]) -> str:
    return(tokenizer.convert_ids_to_tokens(ids))
