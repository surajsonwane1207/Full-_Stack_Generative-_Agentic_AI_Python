import re
from collections import defaultdict
from typing import List, Dict, Tuple

class SimpleBPETokenizer:
    def __init__(self):
        self.vocab: Dict[int, bytes] = {}
        self.merges: Dict[Tuple[int, int], int] = {}
        
    def _get_stats(self, ids: List[int]) -> Dict[Tuple[int, int], int]:
        counts = defaultdict(int)
        for pair in zip(ids, ids[1:]):
            counts[pair] += 1
        return counts

    def _merge(self, ids: List[int], pair: Tuple[int, int], idx: int) -> List[int]:
        newids = []
        i = 0
        while i < len(ids):
            if i < len(ids) - 1 and ids[i] == pair[0] and ids[i+1] == pair[1]:
                newids.append(idx)
                i += 2
            else:
                newids.append(ids[i])
                i += 1
        return newids

    def train(self, text: str, vocab_size: int, verbose: bool = False):
        assert vocab_size >= 256, "Vocab size must be at least 256 for bytes."
        num_merges = vocab_size - 256
        
        # Initialize with raw bytes
        text_bytes = text.encode("utf-8")
        ids = list(text_bytes)
        
        self.vocab = {i: bytes([i]) for i in range(256)}
        self.merges = {}
        
        for i in range(num_merges):
            stats = self._get_stats(ids)
            if not stats:
                break
                
            # Find the most frequent pair
            pair = max(stats, key=stats.get)
            idx = 256 + i
            
            # Merge the pair
            ids = self._merge(ids, pair, idx)
            
            # Record the merge
            self.merges[pair] = idx
            self.vocab[idx] = self.vocab[pair[0]] + self.vocab[pair[1]]
            
            if verbose:
                print(f"Merge {i+1}/{num_merges}: {pair} -> {idx} (count: {stats[pair]})")
                
    def encode(self, text: str) -> List[int]:
        text_bytes = text.encode("utf-8")
        ids = list(text_bytes)
        
        # Apply merges in the order they were learned
        # (A more efficient implementation would use a priority queue or tree, 
        # but this simple loop suffices for basic BPE)
        while len(ids) >= 2:
            stats = self._get_stats(ids)
            # Find the pair that was merged first (has the lowest merge index)
            pair = min(stats.keys(), key=lambda p: self.merges.get(p, float("inf")))
            
            if pair not in self.merges:
                break # No more applicable merges
                
            idx = self.merges[pair]
            ids = self._merge(ids, pair, idx)
            
        return ids

    def decode(self, ids: List[int]) -> str:
        text_bytes = b"".join(self.vocab[idx] for idx in ids)
        return text_bytes.decode("utf-8", errors="replace")
