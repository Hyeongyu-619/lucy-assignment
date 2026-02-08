"""
법률 문서 관련 규칙
"""
import re
from typing import List


class LegalRules:
    """법률 문서 패턴 교정 규칙"""
    
    LEGAL_PAIRS = [
        (r'법\s+령', '법령'), (r'규\s+정', '규정'), (r'조\s+항', '조항'),
        (r'조\s+문', '조문'), (r'단\s+서', '단서'), (r'사\s+항', '사항'),
        (r'요\s+건', '요건'), (r'절\s+차', '절차'), (r'기\s+준', '기준'),
        (r'원\s+칙', '원칙'), (r'예\s+외', '예외'),
    ]
    
    LEGAL_PARTICLES = [
        (r'것으로\s+서', '것으로서'), (r'것으로\s+써', '것으로써'),
        (r'의하\s+여', '의하여'), (r'따\s+라', '따라'),
        (r'관련\s+된', '관련된'), (r'해당하\s+는', '해당하는'),
    ]
    
    @staticmethod
    def apply_all(text: str) -> str:
        """모든 법률 규칙 적용"""
        text = re.sub(r'제\s*(\d+)\s*조', r'제\1조', text)
        text = re.sub(r'제\s*(\d+)\s*항', r'제\1항', text)
        text = re.sub(r'제\s*(\d+)\s*호', r'제\1호', text)
        text = re.sub(r'제\s*(\d+)\s*편', r'제\1편', text)
        text = re.sub(r'제\s*(\d+)\s*장', r'제\1장', text)
        text = re.sub(r'제\s*(\d+)\s*절', r'제\1절', text)
        
        for pattern, replacement in LegalRules.LEGAL_PAIRS:
            text = re.sub(pattern, replacement, text)
        
        for pattern, replacement in LegalRules.LEGAL_PARTICLES:
            text = re.sub(pattern, replacement, text)
        
        return text
    
    @staticmethod
    def apply_to_tokens(tokens: List[str]) -> List[str]:
        """토큰 리스트에 법률 규칙 적용"""
        result = []
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            
            if token == '제' and i + 2 < len(tokens):
                next_token = tokens[i + 1]
                next_next = tokens[i + 2]
                
                if next_token.isdigit() and next_next in ['조', '항', '호', '편', '장', '절']:
                    result.append(f'제{next_token}{next_next}')
                    i += 3
                    continue
                elif next_token.endswith(('조', '항', '호')):
                    result.append(f'제{next_token}')
                    i += 2
                    continue
            
            if token == '법' and i + 1 < len(tokens) and tokens[i + 1] == '령':
                result.append('법령')
                i += 2
                continue
            
            if token == '것으로' and i + 1 < len(tokens) and tokens[i + 1] == '서':
                result.append('것으로서')
                i += 2
                continue
            
            result.append(token)
            i += 1
        
        return result
