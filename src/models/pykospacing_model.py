"""
PyKoSpacing 모델 래퍼
"""
from typing import Optional


class PyKoSpacingModel:
    
    def __init__(self):
        self._spacing = None
        self._available = False
        self._load_model()
    
    def _load_model(self):
        try:
            from pykospacing import Spacing
            self._spacing = Spacing()
            self._available = True
        except (ImportError, Exception):
            pass
    
    def is_available(self) -> bool:
        return self._available
    
    def correct(self, text: str) -> Optional[str]:
        if not self._available or not self._spacing:
            return None
        
        try:
            return self._spacing(text)
        except Exception:
            return None
