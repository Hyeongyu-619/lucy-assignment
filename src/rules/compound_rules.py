"""
합성명사 처리 규칙
"""
import re
from typing import List, Set
from utils.dictionary_loader import DictionaryLoader


class CompoundRules:
    """합성명사 교정 규칙"""
    
    COMMON_SPLITS = [
        ('투자', r'투\s+자'), ('관련', r'관\s+련'), ('비용', r'비\s+용'),
        ('사전', r'사\s+전'), ('수익', r'수\s+익'), ('위험', r'위\s+험'),
        ('법령', r'법\s+령'), ('규정', r'규\s+정'),
    ]
    
    FINANCIAL_PATTERNS = [
        ('투자신탁', r'투자\s*신탁'), ('집합투자기구', r'집합\s*투자\s*기구'),
        ('수익증권', r'수익\s*증권'), ('환매청구', r'환매\s*청구'),
        ('자금납입', r'자금\s*납입'), ('신탁계약', r'신탁\s*계약'),
        ('투자대상', r'투자\s*대상'), ('고위험자산', r'고위험\s*자산'),
        ('순자산', r'순\s*자산'), ('기타비용', r'기타\s*비용'),
        ('성과보수', r'성과\s*보수'), ('운용전문인력', r'운용\s*전문\s*인력'),
        ('이자율변동', r'이자율\s*변동'), ('가격변동', r'가격\s*변동'),
    ]
    
    def __init__(self, dict_loader: DictionaryLoader = None):
        self.dict_loader = dict_loader or DictionaryLoader()
        self._all_terms = None
    
    @property
    def all_terms(self) -> Set[str]:
        if self._all_terms is None:
            self._all_terms = self.dict_loader.get_all_terms()
        return self._all_terms
    
    def fix_compound_nouns(self, text: str) -> str:
        """사전 기반 합성명사 교정"""
        words = text.split()
        result = []
        i = 0
        
        while i < len(words):
            best_match = words[i]
            best_len = 1
            
            for length in range(min(5, len(words) - i), 0, -1):
                candidate = ''.join(words[i:i+length])
                if candidate in self.all_terms and length > 1:
                    best_match = candidate
                    best_len = length
                    break
            
            result.append(best_match)
            i += best_len
        
        return ' '.join(result)
    
    def apply_to_tokens(self, tokens: List[str]) -> List[str]:
        """토큰 리스트에 합성명사 규칙 적용"""
        result = []
        i = 0
        
        while i < len(tokens):
            best_match = tokens[i]
            best_len = 1
            
            for length in range(min(5, len(tokens) - i), 0, -1):
                candidate = ''.join(tokens[i:i+length])
                if candidate in self.all_terms and length > 1:
                    best_match = candidate
                    best_len = length
                    break
            
            result.append(best_match)
            i += best_len
        
        return result
    
    def fix_split_words(self, text: str) -> str:
        """명백하게 잘못 분리된 단어 교정"""
        for replacement, pattern in self.COMMON_SPLITS:
            text = re.sub(pattern, replacement, text)
        
        text = re.sub(r'관\s+련한', '관련한', text)
        text = re.sub(r'관\s+련된', '관련된', text)
        
        return text
    
    def fix_financial_terms(self, text: str) -> str:
        """금융 전문용어 교정"""
        for replacement, pattern in self.FINANCIAL_PATTERNS:
            text = re.sub(pattern, replacement, text)
        return text
