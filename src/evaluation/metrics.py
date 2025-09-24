from typing import Dict, List
from sklearn.metrics import precision_score, recall_score, f1_score

def compute_classification_metrics(y_true: List[int], y_pred: List[int]) -> Dict[str, float]:
    return {
        "precision": precision_score(y_true, y_pred, average="macro", zero_division=0),
        "recall": recall_score(y_true, y_pred, average="macro", zero_division=0),
        "f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
    }

def compute_text_metrics(preds: List[str], refs: List[str]) -> Dict[str, float]:
    # Placeholder: BLEU, ROUGE, etc. (you can plug in nltk/rouge libraries here)
    return {
        "bleu": 0.0,
        "rouge": 0.0,
    }