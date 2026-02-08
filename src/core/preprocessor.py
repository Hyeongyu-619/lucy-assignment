"""
전처리 모듈
"""
import re
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class PreprocessResult:
    text: str
    placeholders: Dict[str, str]
    original_type: str
    
    
class Preprocessor:
    """텍스트 전처리"""
    
    def __init__(self):
        self.placeholder_counter = 0
    
    def preprocess(self, input_data: str | List[str]) -> PreprocessResult:
        """입력 데이터 전처리"""
        original_type = 'list' if isinstance(input_data, list) else 'string'
        text = ' '.join(input_data) if isinstance(input_data, list) else input_data
        text, placeholders = self._extract_protected_patterns(text)
        
        return PreprocessResult(
            text=text,
            placeholders=placeholders,
            original_type=original_type
        )
    
    def _extract_protected_patterns(self, text: str) -> Tuple[str, Dict[str, str]]:
        """보호할 패턴 추출 (URL, 이메일 등)"""
        placeholders = {}
        
        patterns = [
            ('URL', r'https?://[^\s]+'),
            ('EMAIL', r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            ('ABBREV', r'\b[A-Z]{2,}\b'),
        ]
        
        for name, pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                placeholder = f'__{name}_{self.placeholder_counter}__'
                self.placeholder_counter += 1
                placeholders[placeholder] = match
                text = text.replace(match, placeholder, 1)
        
        return text, placeholders
