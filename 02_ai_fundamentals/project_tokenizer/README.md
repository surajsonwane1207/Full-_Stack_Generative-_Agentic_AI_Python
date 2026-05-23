# Project: Tokenizer from Scratch

This project implements a Byte Pair Encoding (BPE) tokenizer from scratch in Python, demonstrating the core algorithm used by many modern Large Language Models (LLMs) such as GPT-3 and LLaMA.

## What is BPE?
Byte Pair Encoding (BPE) is a subword tokenization algorithm that iteratively replaces the most frequent pair of symbols (in our case, raw bytes) in a sequence with a single, new symbol.

## Files
- `tokenizer.py`: Contains the `SimpleBPETokenizer` class which implements the `train`, `encode`, and `decode` methods.
- `main.py`: A demonstration script that trains the tokenizer on a small corpus and tests encoding/decoding on a new sentence.

## How to Run

No external dependencies are required. This uses standard library Python.

```bash
python main.py
```

## How it works
1. **Training**: Starts with a base vocabulary of 256 raw bytes. It scans the corpus, finds the most frequent adjacent pair of bytes, and merges them into a new token. It repeats this until the target vocabulary size is reached.
2. **Encoding**: Converts string text to UTF-8 bytes, then iteratively applies the learned merges to the byte sequence.
3. **Decoding**: Converts the integer token IDs back to their corresponding byte sequences and decodes them to a UTF-8 string.
