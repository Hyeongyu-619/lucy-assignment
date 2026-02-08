"""
후처리 모듈
"""
import re
from typing import List, Dict
from rules.number_rules import NumberRules
from rules.legal_rules import LegalRules
from rules.compound_rules import CompoundRules
from rules.pattern_rules import PatternRules
from utils.dictionary_loader import DictionaryLoader


class Postprocessor:
    """텍스트 후처리"""
    
    def __init__(self, dict_loader: DictionaryLoader = None):
        self.dict_loader = dict_loader or DictionaryLoader()
        self.compound_rules = CompoundRules(self.dict_loader)
    
    def postprocess_string(self, text: str) -> str:
        """문자열 후처리"""
        text = NumberRules.apply_all(text)
        text = LegalRules.apply_all(text)
        text = self.compound_rules.fix_compound_nouns(text)
        text = self.compound_rules.fix_split_words(text)
        text = self.compound_rules.fix_financial_terms(text)
        text = PatternRules.apply_all(text)
        return text
    
    def postprocess_tokens(self, tokens: List[str]) -> List[str]:
        """토큰 리스트 후처리"""
        tokens = NumberRules.apply_to_tokens(tokens)
        tokens = LegalRules.apply_to_tokens(tokens)
        tokens = self.compound_rules.apply_to_tokens(tokens)
        tokens = PatternRules.apply_to_tokens(tokens)
        return [t for t in tokens if t and not t.isspace()]
    
    def convert_to_output_format(
        self, 
        text: str, 
        original_type: str,
        placeholders: Dict[str, str] = None
    ) -> str | List[str]:
        """출력 형식으로 변환"""
        if placeholders:
            for placeholder, original in placeholders.items():
                text = text.replace(placeholder, original)
        
        if original_type == 'string':
            return text
        
        tokens = text.split()
        result = []
        
        for token in tokens:
            if not token:
                continue
            if token in ',.;:!?)]}' and result:
                result[-1] += token
            else:
                result.append(token)
        
        return result
    
    def fine_tune_spacing(self, text: str) -> str:
        """최종 띄어쓰기 미세 조정"""
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'것으로\s+서(?=\s|$|[,.])', '것으로서', text)
        text = re.sub(r'관\s+련', '관련', text)
        text = re.sub(r'비\s+용', '비용', text)
        return text
