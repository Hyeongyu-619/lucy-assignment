"""
한국어 띄어쓰기 교정 시스템 - 메인 모듈
"""
from typing import List, Union
from core.preprocessor import Preprocessor
from core.postprocessor import Postprocessor
from core.validator import Validator
from models.ensemble import EnsembleModel
from utils.dictionary_loader import DictionaryLoader


class SpacingCorrector:
    """띄어쓰기 교정 메인 클래스"""
    
    def __init__(
        self,
        use_pykospacing: bool = True,
        use_kospacing: bool = False,
        use_validator: bool = False,
        dict_dir: str = None
    ):
        self.preprocessor = Preprocessor()
        self.dict_loader = DictionaryLoader(dict_dir)
        self.dict_loader.load_all()
        self.postprocessor = Postprocessor(self.dict_loader)
        self.validator = Validator(use_kiwi=use_validator) if use_validator else None
        self.model = EnsembleModel(
            use_pykospacing=use_pykospacing,
            use_kospacing=use_kospacing
        )
    
    def correct(
        self, 
        input_data: Union[str, List[str]],
        verbose: bool = False
    ) -> Union[str, List[str]]:
        """띄어쓰기 교정"""
        if verbose:
            print(f"[입력 타입] {type(input_data).__name__}")
        
        preprocess_result = self.preprocessor.preprocess(input_data)
        corrected = self.model.correct(preprocess_result.text)
        
        corrected = self.postprocessor.postprocess_string(corrected)
        corrected = self.postprocessor.fine_tune_spacing(corrected)
        
        if preprocess_result.original_type == 'list':
            tokens = corrected.split()
            tokens = self.postprocessor.postprocess_tokens(tokens)
            corrected = ' '.join(tokens)
        
        if self.validator and verbose:
            is_valid, warnings_list = self.validator.validate(corrected)
            if not is_valid:
                print(f"[검증 경고] {warnings_list}")
        
        result = self.postprocessor.convert_to_output_format(
            corrected,
            preprocess_result.original_type,
            preprocess_result.placeholders
        )
        
        return result
    
    def batch_correct(
        self, 
        inputs: List[Union[str, List[str]]],
        verbose: bool = False
    ) -> List[Union[str, List[str]]]:
        """배치 교정"""
        return [self.correct(input_data, verbose=verbose) for input_data in inputs]
    
    def get_info(self) -> dict:
        """시스템 정보"""
        return {
            'models': self.model.get_available_models() if self.model else [],
            'dictionaries': {
                'compound_nouns': len(self.dict_loader.compound_nouns),
                'financial_terms': len(self.dict_loader.financial_terms),
                'legal_terms': len(self.dict_loader.legal_terms),
                'proper_nouns': len(self.dict_loader.proper_nouns),
            },
            'validator_enabled': self.validator is not None,
        }


def correct_spacing(input_data: Union[str, List[str]], **kwargs) -> Union[str, List[str]]:
    """띄어쓰기 교정 간편 함수"""
    corrector = SpacingCorrector(**kwargs)
    return corrector.correct(input_data)
