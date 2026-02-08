"""
평가 지표 계산
"""
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class SpacingMetrics:
    accuracy: float
    char_f1: float
    word_f1: float
    precision: float
    recall: float
    
    def __str__(self) -> str:
        return (
            f"정확도: {self.accuracy:.1%}, Char F1: {self.char_f1:.1%}, "
            f"Word F1: {self.word_f1:.1%}, Precision: {self.precision:.1%}, Recall: {self.recall:.1%}"
        )


def calculate_metrics(predictions: List[str], references: List[str]) -> SpacingMetrics:
    """띄어쓰기 교정 평가 지표 계산"""
    if len(predictions) != len(references) or not predictions:
        return SpacingMetrics(0.0, 0.0, 0.0, 0.0, 0.0)
    
    exact_matches = sum(1 for p, r in zip(predictions, references) if p == r)
    accuracy = exact_matches / len(predictions)
    
    char_metrics = [_calculate_char_metrics(p, r) for p, r in zip(predictions, references)]
    total_tp = sum(m[0] for m in char_metrics)
    total_fp = sum(m[1] for m in char_metrics)
    total_fn = sum(m[2] for m in char_metrics)
    
    char_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    char_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    char_f1 = 2 * char_precision * char_recall / (char_precision + char_recall) if (char_precision + char_recall) > 0 else 0.0
    
    word_metrics = [_calculate_word_metrics(p, r) for p, r in zip(predictions, references)]
    total_tp_word = sum(m[0] for m in word_metrics)
    total_fp_word = sum(m[1] for m in word_metrics)
    total_fn_word = sum(m[2] for m in word_metrics)
    
    word_precision = total_tp_word / (total_tp_word + total_fp_word) if (total_tp_word + total_fp_word) > 0 else 0.0
    word_recall = total_tp_word / (total_tp_word + total_fn_word) if (total_tp_word + total_fn_word) > 0 else 0.0
    word_f1 = 2 * word_precision * word_recall / (word_precision + word_recall) if (word_precision + word_recall) > 0 else 0.0
    
    return SpacingMetrics(
        accuracy=accuracy,
        char_f1=char_f1,
        word_f1=word_f1,
        precision=char_precision,
        recall=char_recall
    )


def _calculate_char_metrics(pred: str, ref: str) -> Tuple[int, int, int]:
    """문자 단위 TP, FP, FN 계산"""
    pred_chars = [c for c in pred if c != ' ']
    ref_chars = [c for c in ref if c != ' ']
    
    if pred_chars != ref_chars:
        return 0, len([c for c in pred if c == ' ']), len([c for c in ref if c == ' '])
    
    pred_spaces = {i for i, c in enumerate(pred_chars[:-1]) if pred[pred.index(pred_chars[i]) + 1] == ' '}
    ref_spaces = {i for i, c in enumerate(ref_chars[:-1]) if ref[ref.index(ref_chars[i]) + 1] == ' '}
    
    tp = len(pred_spaces & ref_spaces)
    fp = len(pred_spaces - ref_spaces)
    fn = len(ref_spaces - pred_spaces)
    
    return tp, fp, fn


def _calculate_word_metrics(pred: str, ref: str) -> Tuple[int, int, int]:
    """어절 단위 TP, FP, FN 계산"""
    pred_words = set(pred.split())
    ref_words = set(ref.split())
    
    tp = len(pred_words & ref_words)
    fp = len(pred_words - ref_words)
    fn = len(ref_words - pred_words)
    
    return tp, fp, fn


def calculate_single_accuracy(pred: str, ref: str) -> bool:
    """단일 문장 정확도"""
    return pred == ref


def calculate_error_rate(predictions: List[str], references: List[str]) -> float:
    """오류율 계산"""
    if not predictions:
        return 1.0
    errors = sum(1 for p, r in zip(predictions, references) if p != r)
    return errors / len(predictions)
