"""
숫자 관련 띄어쓰기 규칙
"""
import re
from typing import List


class NumberRules:
    """숫자 패턴 교정 규칙"""
    
    @staticmethod
    def apply_all(text: str) -> str:
        """모든 숫자 규칙 적용"""
        text = re.sub(r'(\d)\s+(\d)', r'\1\2', text)
        text = re.sub(r'(\d+)\s*,\s*(\d{3})', r'\1,\2', text)
        text = re.sub(r'(\d)\s*\.\s*(\d)', r'\1.\2', text)
        text = re.sub(r'(\d)\s*%', r'\1%', text)
        
        units = ['원', '좌', '주', '구', '건', '개', '명', '인', '일', '년', '월', '회', '차', '호']
        for unit in units:
            text = re.sub(rf'(\d)\s+{unit}', rf'\1{unit}', text)
        
        text = re.sub(r'(\d)\s*~\s*(\d)', r'\1~\2', text)
        text = re.sub(r'(\d)\s*-\s*(\d)', r'\1-\2', text)
        
        return text
    
    @staticmethod
    def apply_to_tokens(tokens: List[str]) -> List[str]:
        """토큰 리스트에 숫자 규칙 적용"""
        result = []
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            
            if token.isdigit():
                merged = token
                j = i + 1
                
                while j < len(tokens):
                    next_token = tokens[j]
                    
                    if next_token.isdigit() or next_token == ',':
                        merged += next_token
                        j += 1
                    elif next_token in ['%', '원', '좌', '주', '개', '명'] or \
                         next_token.startswith('%') or next_token.startswith('원'):
                        merged += next_token
                        j += 1
                        break
                    else:
                        break
                
                result.append(merged)
                i = j
            else:
                result.append(token)
                i += 1
        
        return result
