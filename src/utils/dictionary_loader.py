"""
사전 로더
"""
from typing import Set
from pathlib import Path


class DictionaryLoader:
    """사전 파일 로더"""
    
    def __init__(self, dict_dir: str = None):
        if dict_dir is None:
            current_file = Path(__file__)
            project_root = current_file.parent.parent.parent
            dict_dir = project_root / "data" / "dictionaries"
        
        self.dict_dir = Path(dict_dir)
        self._compound_nouns: Set[str] = set()
        self._financial_terms: Set[str] = set()
        self._legal_terms: Set[str] = set()
        self._proper_nouns: Set[str] = set()
        
    def load_all(self) -> None:
        """모든 사전 로드"""
        self._compound_nouns = self._load_dict_file("compound_nouns.txt")
        self._financial_terms = self._load_dict_file("financial_terms.txt")
        self._legal_terms = self._load_dict_file("legal_terms.txt")
        self._proper_nouns = self._load_dict_file("proper_nouns.txt")
    
    def _load_dict_file(self, filename: str) -> Set[str]:
        """사전 파일 로드"""
        filepath = self.dict_dir / filename
        terms = set()
        
        if not filepath.exists():
            return terms
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    terms.add(line)
        
        return terms
    
    @property
    def compound_nouns(self) -> Set[str]:
        if not self._compound_nouns:
            self.load_all()
        return self._compound_nouns
    
    @property
    def financial_terms(self) -> Set[str]:
        if not self._financial_terms:
            self.load_all()
        return self._financial_terms
    
    @property
    def legal_terms(self) -> Set[str]:
        if not self._legal_terms:
            self.load_all()
        return self._legal_terms
    
    @property
    def proper_nouns(self) -> Set[str]:
        if not self._proper_nouns:
            self.load_all()
        return self._proper_nouns
    
    def get_all_terms(self) -> Set[str]:
        return (self.compound_nouns | self.financial_terms | 
                self.legal_terms | self.proper_nouns)
