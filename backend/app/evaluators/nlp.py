from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _simple_bleu(reference: str, hypothesis: str) -> float:
    ref_tokens = reference.split()
    hyp_tokens = hypothesis.split()
    if not hyp_tokens:
        return 0.0
    overlap = sum(1 for token in hyp_tokens if token in ref_tokens)
    return overlap / len(hyp_tokens)


def evaluate_nlp(y_true: list[Any], y_pred: list[Any]) -> dict[str, float]:
    references = [str(item) for item in y_true]
    hypotheses = [str(item) for item in y_pred]

    bleu_scores = [_simple_bleu(ref, hyp) for ref, hyp in zip(references, hypotheses)]

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(references + hypotheses)
    ref_vecs = matrix[: len(references)]
    pred_vecs = matrix[len(references) :]
    cosine_scores = np.diag(cosine_similarity(ref_vecs, pred_vecs))

    return {
        "bleu": float(np.mean(bleu_scores) if bleu_scores else 0.0),
        "cosine_similarity": float(np.mean(cosine_scores) if len(cosine_scores) else 0.0),
    }
