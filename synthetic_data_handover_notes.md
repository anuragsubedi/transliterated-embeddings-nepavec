# Handover Notes: Romanized Nepali Word2Vec Project

## Project Goal
Building a Word2Vec embedding model from scratch in PyTorch for Romanized Nepali. The model aims to capture semantic meaning despite the messy, inconsistent nature of real-world transliterated typing.

## Dataset Information
A synthetic dataset of **1,000 sentences** has been generated to serve as the initial training data.

### Storage Location
- **Directory:** `dataset/`
- **Files:** `chunk_1.json` to `chunk_20.json` (20 files total).
- **Format:** Each file contains a JSON array of exactly 50 strings.

### Dataset Composition
The data was synthesized to cover three distinct linguistic tones and incorporate intentional "noise" for robustness:

1.  **Street/Slang (Chunks 1-5):** Highly informal, abbreviations, and modern slang (e.g., "Oye bro", "khatra", "jhoppo").
2.  **Formal/Polite (Chunks 6-10):** Respectful, standard grammar (e.g., "Namaste", "Tapai", "Hajur").
3.  **Academic/Professional (Chunks 11-15):** Conceptual and vocabulary-rich (e.g., "Siddhanta", "Arthik bikas", "Rajnaitik sthirta").
4.  **Mixed Variations (Chunks 16-20):** Combined tones with phonetic variations (e.g., `chha` vs `cha`, `parcha` vs `parxa`, `bhako` vs `vako`).

### Linguistic Rules Followed
- **Romanized Nepali Only:** No Devanagari script.
- **Anti-Gibberish:** No repeating character loops; every word has semantic meaning.
- **Transliteration Noise:** Intentional spelling inconsistencies to mimic real-world typing.

## Current Progress
- [x] Create `dataset/` directory.
- [x] Generate 1,000 sentences (20 chunks).
- [x] Verify data integrity (JSON validity and sentence counts).
- [x] Verify linguistic constraints.

## Next steps for the Agent
1.  **Preprocessing:** Tokenize the sentences in the `dataset/*.json` files. Consider a custom tokenizer or a subword tokenizer (like SentencePiece) to handle spelling variations.
2.  **Vocabulary Building:** Create a vocabulary mapping from the 1,000 sentences.
3.  **Model Architecture:** Implement the Word2Vec (Skip-gram or CBOW) architecture in PyTorch.
4.  **Training:** Train the embeddings on the generated dataset.
5.  **Evaluation:** Test the embeddings on semantic similarity tasks specific to Romanized Nepali.

## Loading the Data
Example Python snippet for the next agent to load the data:

```python
import json
import glob

def load_dataset(pattern="dataset/chunk_*.json"):
    all_sentences = []
    for filepath in sorted(glob.glob(pattern)):
        with open(filepath, 'r') as f:
            all_sentences.extend(json.load(f))
    return all_sentences

# Usage:
# sentences = load_dataset()
# print(f"Loaded {len(sentences)} sentences.")
```
