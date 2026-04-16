# Romanized Nepali Embeddings

While Romanized Nepali text dominates digital communication, SMS, and social media across Nepal, it remains a critically under-resourced domain in Natural Language Processing (NLP). The primary research gap in transliterated NLP stems from a complete lack of orthographic standardization; users type phonetically, resulting in extreme spelling variations (e.g.,  *chha* ,  *cha* ,  *xa* ) and frequent code-switching. This phonetic "noise" leads to massive Out-Of-Vocabulary (OOV) rates that easily break traditional NLP pipelines.

This project aims to dissect and address these transliteration challenges from first principles. By first synthesizing a controlled, phonetically variable dataset, we construct a ground-up embedding pipeline. We begin by building a Word2Vec architecture from scratch to empirically demonstrate the limitations of static word vectors when faced with spelling inconsistencies. We then progressively advance the architecture through Recurrent Neural Networks (RNNs), subword tokenization, and modern attention mechanisms. Ultimately, this project serves as a practical, step-by-step exploration of how modern contextual architectures overcome the unstructured reality of low-resource, transliterated languages.

## Phase 0: Synthetic Data Generation & Structuring

Before building the architecture, a controlled dataset of 1,000 Romanized Nepali sentences was synthesized using an LLM to mimic real-world typing behavior without triggering LLM degradation.

- **Step 1: Agentic Orchestration:** Utilized a stateless, agentic loop (via Google Antigravity) to generate data in isolated batches. This prevented the autoregressive "repetition trap" commonly caused by forcing LLMs to generate noisy text in a continuous context window.
- **Step 2: Linguistic Variation & "Noise" Injection:** Intentionally mapped real-world transliteration variations (e.g., _cha/chha/xa_, _timi/tme_) directly into the text generation. The data was strictly balanced across three semantic tones: Street/Slang, Formal/Polite, and Academic/Professional.
- **Step 3: Chunked Storage:** The output was constrained to valid JSON arrays and partitioned into 20 distinct files (`dataset/chunk_1.json` through `dataset/chunk_20.json`, containing 50 sentences each) for safe loading and memory-efficient I/O.

## Phase 1: The Foundation (Data Prep & Naïve Tokenization)

Before neural networks can learn, they need numbers. This phase transforms the raw JSON text into a mathematical vocabulary.

- **Step 1: Data Loader:** Implement a PyTorch `Dataset` and `DataLoader` to stream the sentences from the `dataset/chunk_X.json` files.
- **Step 2: Basic Cleaning:** Lowercase all text and strip out extraneous punctuation.
- **Step 3: Whitespace Tokenization:** Split the sentences into discrete words based on spaces.
- **Step 4: Vocabulary Mapping:** Create two Python dictionaries: `word_to_index` (e.g., `{"khatra": 42}`) and `index_to_word` (`{42: "khatra"}`). Determine the absolute vocabulary size ($V$).

## Phase 2: The Classic Word Embedding (Word2Vec Skip-Gram)

Building the foundational lookup table to capture semantic similarity at the word level.

- **Step 1: Generate Training Pairs:** Write a sliding window function to create (Target Word, Context Word) pairs from the tokenized sentences.
- **Step 2: PyTorch Architecture:** Build a shallow neural network with exactly one hidden layer.

  - _Input:_ One-hot encoded vector of size $V$.
  - _Hidden Layer:_ Linear layer of size $N$ (e.g., 50 dimensions). **This is the embedding matrix.**
  - _Output:_ Linear layer of size $V$ with a Softmax activation to predict the context word.
- **Step 3: Training Loop:** Train the model using Cross-Entropy Loss and an optimizer (like Adam).
- **Step 4: Evaluation (Cosine Similarity):** Extract the hidden layer weights and write a function to find the "closest" words to a given input (e.g., does the vector for "ramro" sit close to "rmro" and "thik"?).

## Phase 3: The Sentence Problem (Sequence & Order)

Word2Vec doesn't understand sentences. This phase bridges the gap between static words and contextual meaning.

- **Step 1: The Baseline (Bag of Words):** Create a naïve sentence embedding by mathematically averaging the Word2Vec vectors of the words within a sentence. Observe its failure to capture word order (e.g., "Kukur le manche tokyo" vs. "Manche le kukur tokyo").
- **Step 2: Introduction to Recurrent Neural Networks (RNN/LSTM):** Build a basic PyTorch LSTM. Pass the Word2Vec embeddings into the LSTM sequentially so the network can maintain a "hidden state" memory of the word order.

## Phase 4: Advanced Tokenization (Solving the "Noise")

Basic whitespace tokenization treats "chha", "cha", and "xa" as three completely unrelated words. To fix this, we upgrade the tokenizer.

- **Step 1: Subword Tokenization:** Implement Byte-Pair Encoding (BPE) or use the `SentencePiece` library.
- **Step 2: Subword Mapping:** Train the tokenizer to break words into phonetic chunks (e.g., "khatra" -> `["kha", "tra"]`). This allows the model to realize that "bhaako" and "bhako" share the root subword "bha".

## Phase 5: The Modern Era (Encoder-Decoder & Attention)

Moving away from static embeddings entirely and stepping into the architecture that powers modern LLMs.

- **Step 1: The Seq2Seq Architecture:** Build a basic Encoder-Decoder model. Use the Encoder to compress a Romanized Nepali sentence into a single "context vector", and the Decoder to try and reconstruct it (an autoencoder setup).
- **Step 2: The Attention Mechanism:** Implement scaled dot-product attention. Instead of compressing the sentence into one vector, allow the Decoder to "look back" at specific words in the input sequence at every step.
- **Step 3: A Mini-Transformer:** Strip away the RNNs entirely and build a small Transformer Encoder block (Self-Attention + Feed Forward) to generate truly contextualized embeddings for the Romanized Nepali sentences.
