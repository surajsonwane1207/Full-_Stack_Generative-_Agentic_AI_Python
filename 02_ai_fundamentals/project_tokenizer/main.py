from tokenizer import SimpleBPETokenizer

def main():
    print("--- Training BPE Tokenizer ---")
    
    # Sample corpus
    corpus = """
    Large language models rely heavily on tokenization.
    Tokenization is the process of breaking text into smaller subword units.
    Byte pair encoding (BPE) is a popular subword tokenization algorithm.
    It iteratively merges the most frequent pairs of characters or bytes.
    """
    
    # Initialize and train
    tokenizer = SimpleBPETokenizer()
    vocab_size = 256 + 20 # 256 base bytes + 20 merges
    tokenizer.train(corpus, vocab_size=vocab_size, verbose=True)
    
    print("\n--- Testing Tokenizer ---")
    test_text = "Tokenization relies on byte pair encoding."
    print(f"Original Text: '{test_text}'")
    
    # Encode
    encoded_ids = tokenizer.encode(test_text)
    print(f"Encoded IDs: {encoded_ids}")
    
    # Decode
    decoded_text = tokenizer.decode(encoded_ids)
    print(f"Decoded Text: '{decoded_text}'")
    
    assert test_text == decoded_text, "Decoding failed to reproduce the original string!"
    print("\nSuccess! The tokenizer successfully encodes and decodes text.")

if __name__ == "__main__":
    main()
