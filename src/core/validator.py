"""
형태소 분석 기반 검증
"""
import re
import warnings
from typing import List, Tuple


class Validator:
    """띄어쓰기 결과 검증"""
    
    def __init__(self, use_kiwi: bool = False):
        self.use_kiwi = use_kiwi
        self._kiwi = None
        
        if use_kiwi:
            try:
                from kiwipiepy import Kiwi
                self._kiwi = Kiwi()
            except ImportError:
                warnings.warn("Kiwi를 불러올 수 없습니다.")
                self.use_kiwi = False
    
    def validate(self, text: str) -> Tuple[bool, List[str]]:
        """띄어쓰기 결과 검증"""
        warnings_list = []
        warnings_list.extend(self._basic_validation(text))
        
        if self.use_kiwi and self._kiwi:
            warnings_list.extend(self._morphological_validation(text))
        
        return (len(warnings_list) == 0, warnings_list)
    
    def _basic_validation(self, text: str) -> List[str]:
        """기본 검증"""
        warnings = []
        
        if re.search(r'\s{2,}', text):
            warnings.append("중복 공백이 있습니다")
        
        if text.startswith(' ') or text.endswith(' '):
            warnings.append("문장 시작/끝에 공백이 있습니다")
        
        if re.search(r'\d\s+\d', text):
            warnings.append("숫자 사이에 공백이 있습니다")
        
        if re.search(r'제\s+\d', text):
            warnings.append("법령 번호에 공백이 있습니다")
        
        return warnings
    
    def _morphological_validation(self, text: str) -> List[str]:
        """형태소 분석 기반 검증"""
        warnings = []
        
        if not self._kiwi:
            return warnings
        
        try:
            result = self._kiwi.analyze(text)
            if not result:
                return warnings
            
            tokens = result[0][0]
            unknown_count = sum(1 for token in tokens if token.tag == 'UN')
            if unknown_count > len(tokens) * 0.3:
                warnings.append(f"미등록어가 많습니다 ({unknown_count}/{len(tokens)})")
        except Exception as e:
            warnings.append(f"형태소 분석 중 오류: {str(e)}")
        
        return warnings
