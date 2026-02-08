"""
텍스트 처리 유틸리티
"""
import re
from typing import List


def list_to_string(tokens: List[str]) -> str:
    """토큰 리스트를 문자열로 결합"""
    return ''.join(tokens)


def string_to_list(text: str) -> List[str]:
    """문자열을 토큰 리스트로 분리"""
    return text.split()


def normalize_spacing(text: str) -> str:
    """다중 공백을 단일 공백으로 정규화"""
    return re.sub(r'\s+', ' ', text).strip()


def remove_all_spaces(text: str) -> str:
    """모든 공백 제거"""
    return re.sub(r'\s+', '', text)
