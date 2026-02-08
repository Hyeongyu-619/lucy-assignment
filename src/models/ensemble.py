"""
앙상블 모델
"""
import re
from typing import List
from models.pykospacing_model import PyKoSpacingModel
from models.kospacing_model import KoSpacingModel


class EnsembleModel:
    """띄어쓰기 교정 모델 앙상블"""
    
    def __init__(self, use_pykospacing: bool = True, use_kospacing: bool = False):
        self.models = []
        
        if use_pykospacing:
            pyk = PyKoSpacingModel()
            if pyk.is_available():
                self.models.append(('pykospacing', pyk))
        
        if use_kospacing:
            kos = KoSpacingModel()
            if kos.is_available():
                self.models.append(('kospacing', kos))
    
    def correct(self, text: str, method: str = 'vote') -> str:
        """교정 실행"""
        if not self.models:
            return re.sub(r'\s+', ' ', text).strip()
        
        if len(self.models) == 1:
            _, model = self.models[0]
            result = model.correct(text)
            return result if result else text
        
        results = [model.correct(text) for _, model in self.models if model.correct(text)]
        return results[0] if results else text
    
    def get_available_models(self) -> List[str]:
        return [name for name, _ in self.models]
