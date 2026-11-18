# Lexical Profile of Kazakh Legal Language

## Project Overview

This project explores the lexical and morphological
characteristics of Kazakh legal document metadata
using Python, Natural Language Processing (NLP),
SQL, and information retrieval techniques.

The analysis uses titles and descriptions of legal
documents, rather than full legislative texts.

## Dataset

- Documents: 215,889
- Source file: kazakhlawcorpus_kk_only.csv
- Original format: CSV
- Optimized format: Parquet
- Main text fields: title and description

The corpus contains legal document metadata
spanning multiple decades.

The dataset is predominantly Kazakh-language,
but some records may contain Russian or mixed-language
text. Language detection was preliminary and was
not fully manually validated.

## Technologies

- Python 3.13
- pandas and NumPy
- PyArrow and Parquet
- SQLite
- scikit-learn
- KazStem 0.2.1
- Matplotlib and SciPy

See requirements.txt for installed package versions.

## Methods

### 1. Data Preparation

- Dataset inspection
- Missing-value analysis
- Duplicate analysis
- Unicode normalization
- CSV-to-Parquet conversion
- Memory and reading performance comparison

### 2. Lexical Analysis

- Cyrillic tokenization
- Word frequency analysis
- Stopword analysis
- Zipf's Law
- Bigram and trigram analysis
- Temporal lexical analysis

### 3. Morphological Analysis

KazStem was used for conservative morphological
normalization.

When a token had one unique candidate lemma,
that lemma was selected.

When multiple candidate lemmas were returned,
the original token was retained.

### 4. SQL Analysis

A SQLite database was created containing
215,889 legal documents.

Eight SQL queries demonstrate filtering,
aggregation, conditional classification,
common table expressions, and joins.

### 5. TF-IDF Information Retrieval

Two search models were developed:

- Baseline TF-IDF
- Lemma-based TF-IDF

Both models index legal document titles.

Retrieval uses cosine similarity.

## Main Results

### Tokenization

- Title tokens: 3,965,957
- Description tokens: 3,681,040
- Combined occurrences: 7,646,997

### Vocabulary Reduction

| Corpus | Original | Normalized | Reduction |
|---|---:|---:|---:|
| Titles | 34,361 | 22,944 | 33.23% |
| Descriptions | 4,476 | 3,912 | 12.60% |
| Combined | 35,523 | 23,967 | 32.53% |

### TF-IDF Features

- Baseline: 22,732 features
- Lemma-based: 14,535 features
- Feature reduction: 36.06%

### Search Evaluation

Preliminary mean Precision@5 across five
selected legal queries:

- Baseline TF-IDF: 0.64
- Lemma-based TF-IDF: 0.80

The reported relevance judgments were based
primarily on document titles.

## Limitations

1. The dataset contains document titles and
   descriptions, not full legislative texts.

2. Language classification has not undergone
   complete manual verification.

3. Cyrillic tokenization removes digits and
   punctuation, which can affect n-grams.

4. Morphological normalization can introduce
   errors, especially for proper names and
   ambiguous word forms.

5. The 50-form lemmatization audit was prepared,
   but its formal accuracy metric has not been
   finalized.

6. Search evaluation uses only five queries and
   preliminary title-based relevance judgments.

7. Temporal patterns may reflect changes in
   corpus composition and document coverage.

## Reproducibility

Python dependencies are listed in requirements.txt.

The optimized dataset, SQLite database, TF-IDF
models, lemma mapping, and evaluation results
are stored in the project directory.

The saved TF-IDF models were successfully
reloaded and tested in the existing Colab
environment.

KazStem requires additional FST resources
not installed through pip alone.

For KazStem 0.2.1, the matching Ubuntu 24.04
release bundle was downloaded and its SHA-256
checksum verified before resource extraction.

A complete fresh-environment reproduction
test has not yet been performed.

## Project Structure

data/
  raw/
  processed/
  database/

models/

outputs/
  figures/

requirements.txt
README.md

## Conclusion

Morphological normalization substantially
reduces the feature space of Kazakh legal
document representations.

In the preliminary search evaluation,
lemma-based TF-IDF achieved higher mean
Precision@5 than the baseline model.

These findings motivate further evaluation
with more queries, independent relevance
judgments, and additional linguistic validation.
