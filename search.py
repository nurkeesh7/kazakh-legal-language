import re
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

PATTERN = re.compile(r"[а-яёәғқңөұүһі]+", re.IGNORECASE)


def load_search_system(project_dir):
    project_dir = Path(project_dir)
    model_dir = project_dir / "models"

    models = {}

    for name, prefix in [
        ("Baseline", "tfidf"),
        ("Lemma-based", "lemma_tfidf")
    ]:
        models[name] = {
            "vectorizer": joblib.load(
                model_dir / f"{prefix}_vectorizer.joblib"
            ),
            "matrix": joblib.load(
                model_dir / f"{prefix}_matrix.joblib"
            ),
            "documents": pd.read_parquet(
                model_dir / f"{prefix}_documents.parquet"
            )
        }

    mapping = pd.read_parquet(
        project_dir / "data/processed/kazstem_lemma_mapping.parquet"
    )

    lemma_map = dict(zip(mapping["word"], mapping["lemma"]))

    return models, lemma_map


def preprocess_query(query, lemma_map, use_lemmas=False):
    tokens = PATTERN.findall(query.lower())

    if use_lemmas:
        tokens = [lemma_map.get(token, token) for token in tokens]

    return " ".join(tokens)


def search_documents(query, models, lemma_map,
                     model_name="Lemma-based", top_k=5):

    if model_name not in models:
        raise ValueError("Unknown model")

    if not 1 <= top_k <= 20:
        raise ValueError("top_k must be between 1 and 20")

    model = models[model_name]

    cleaned = preprocess_query(
        query,
        lemma_map,
        model_name == "Lemma-based"
    )

    query_vector = model["vectorizer"].transform([cleaned])

    if query_vector.nnz == 0:
        return pd.DataFrame()

    scores = (model["matrix"] @ query_vector.T).toarray().ravel()
    candidates = np.flatnonzero(scores > 0)

    if len(candidates) == 0:
        return pd.DataFrame()

    k = min(top_k, len(candidates))

    selected = np.argpartition(
        scores[candidates], -k
    )[-k:]

    indices = candidates[selected]
    indices = indices[np.argsort(-scores[indices], kind="stable")]

    results = model["documents"].iloc[indices].copy()
    results["similarity"] = np.round(scores[indices], 4)

    return results.reset_index(drop=True)
