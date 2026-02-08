"""
일반 패턴 기반 규칙
"""
import re
from typing import List


class PatternRules:
    """패턴 기반 교정 규칙"""
    
    @staticmethod
    def apply_all(text: str) -> str:
        """모든 패턴 규칙 적용"""
        text = re.sub(r'\(\s+', '(', text)
        text = re.sub(r'\s+\)', ')', text)
        text = re.sub(r'\[\s+', '[', text)
        text = re.sub(r'\s+\]', ']', text)
        text = re.sub(r'\(([가-힣]{3,})([가-힣]{2,})', r'\1(\2', text)
        
        text = re.sub(r'\s+,', ',', text)
        text = re.sub(r'\s+\.', '.', text)
        text = re.sub(r'･\s+', '･', text)
        text = re.sub(r'\s+･', '･', text)
        text = re.sub(r'\s+:', ':', text)
        text = re.sub(r'\s+;', ';', text)
        
        text = re.sub(r'"\s+', '"', text)
        text = re.sub(r'\s+"', '"', text)
        text = re.sub(r"'\s+", "'", text)
        text = re.sub(r"\s+'", "'", text)
        
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def apply_to_tokens(tokens: List[str]) -> List[str]:
        """토큰 리스트에 패턴 규칙 적용"""
        result = []
        
        for token in tokens:
            if not token or token.isspace():
                continue
            
            if token in [',', '.', ')', ']', '}'] and result:
                result[-1] += token
            else:
                result.append(token)
        
        return result
