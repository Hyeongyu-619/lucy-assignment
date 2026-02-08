"""
제공된 예시에 대한 테스트
"""
import json
import sys
from pathlib import Path

# src 디렉토리를 path에 추가
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from core.spacing_corrector import SpacingCorrector
from utils.metrics import calculate_single_accuracy


# 테스트 데이터 로드
def load_examples():
    """제공된 예시 로드"""
    data_path = Path(__file__).parent.parent / "data" / "examples" / "provided_examples.json"
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture(scope="module")
def corrector():
    """SpacingCorrector 인스턴스"""
    return SpacingCorrector(
        use_pykospacing=True,
        use_kospacing=False,
        use_validator=False
    )


@pytest.fixture(scope="module")
def examples():
    """테스트 예시"""
    return load_examples()


def test_corrector_initialization(corrector):
    """교정기 초기화 테스트"""
    assert corrector is not None
    info = corrector.get_info()
    print(f"\n사용 가능한 모델: {info['models']}")
    assert info['dictionaries']['compound_nouns'] > 0


def test_example_1(corrector, examples):
    """예시 1: 관 련한 → 관련한"""
    ex = examples[0]
    result = corrector.correct(ex['input'])
    
    print(f"\n[예시 1]")
    print(f"입력: {ex['input'][:10]}...")
    print(f"예상: {ex['expected_output'][:10]}...")
    print(f"결과: {result[:10]}...")
    
    # 완전 일치 확인
    is_correct = (result == ex['expected_output'])
    print(f"정확도: {'✓ 정확' if is_correct else '✗ 불일치'}")
    
    # 주요 이슈 확인
    if isinstance(result, list):
        result_str = ''.join(result)
    else:
        result_str = result
    
    assert '관련한' in result_str, "관 련한 → 관련한 교정 실패"


def test_example_2(corrector, examples):
    """예시 2: 사 전에 → 사전에"""
    ex = examples[1]
    result = corrector.correct(ex['input'])
    
    print(f"\n[예시 2]")
    print(f"입력: {ex['input']}")
    print(f"예상: {ex['expected_output']}")
    print(f"결과: {result}")
    
    if isinstance(result, list):
        result_str = ''.join(result)
    else:
        result_str = result
    
    assert '사전에' in result_str, "사 전에 → 사전에 교정 실패"


def test_example_3(corrector, examples):
    """예시 3: 수 익자가 → 수익자가"""
    ex = examples[2]
    result = corrector.correct(ex['input'])
    
    print(f"\n[예시 3]")
    print(f"입력: {ex['input'][:5]}...")
    print(f"예상: {ex['expected_output'][:5]}...")
    print(f"결과: {result[:5]}...")
    
    if isinstance(result, list):
        result_str = ''.join(result)
    else:
        result_str = result
    
    assert '수익자가' in result_str, "수 익자가 → 수익자가 교정 실패"


def test_example_4(corrector, examples):
    """예시 4: 비 용 → 비용, 괄호 교정"""
    ex = examples[3]
    result = corrector.correct(ex['input'])
    
    print(f"\n[예시 4]")
    print(f"입력: {ex['input'][:10]}...")
    print(f"예상: {ex['expected_output'][:10]}...")
    print(f"결과: {result[:10]}...")
    
    if isinstance(result, list):
        result_str = ''.join(result)
    else:
        result_str = result
    
    assert '비용' in result_str, "비 용 → 비용 교정 실패"


def test_example_5(corrector, examples):
    """예시 5: 8 0% → 80%"""
    ex = examples[4]
    result = corrector.correct(ex['input'])
    
    print(f"\n[예시 5]")
    print(f"입력: {ex['input']}")
    print(f"예상: {ex['expected_output']}")
    print(f"결과: {result}")
    
    if isinstance(result, list):
        result_str = ''.join(result)
    else:
        result_str = result
    
    assert '80%' in result_str or ('80%이상' in result_str), "8 0% → 80% 교정 실패"


def test_example_6(corrector, examples):
    """예시 6: 정상 케이스"""
    ex = examples[5]
    result = corrector.correct(ex['input'])
    
    print(f"\n[예시 6]")
    print(f"입력: {ex['input'][:5]}...")
    print(f"예상: {ex['expected_output'][:5]}...")
    print(f"결과: {result[:5]}...")


def test_example_7(corrector, examples):
    """예시 7: 것으로 서 → 것으로서"""
    ex = examples[6]
    result = corrector.correct(ex['input'])
    
    print(f"\n[예시 7]")
    print(f"입력: {ex['input'][:10]}...")
    print(f"예상: {ex['expected_output'][:10]}...")
    print(f"결과: {result[:10]}...")
    
    if isinstance(result, list):
        result_str = ''.join(result)
    else:
        result_str = result
    
    assert '것으로서' in result_str, "것으로 서 → 것으로서 교정 실패"


def test_example_string_1(corrector, examples):
    """문자열 예시 1: 법 령 → 법령"""
    ex = examples[7]
    result = corrector.correct(ex['input'])
    
    print(f"\n[문자열 예시 1]")
    print(f"입력: {ex['input']}")
    print(f"예상: {ex['expected_output']}")
    print(f"결과: {result}")
    
    assert isinstance(result, str), "문자열 입력은 문자열로 반환되어야 함"
    assert '법령' in result, "법 령 → 법령 교정 실패"


def test_example_string_2(corrector, examples):
    """문자열 예시 2: 투 자신탁으로 → 투자신탁으로"""
    ex = examples[8]
    result = corrector.correct(ex['input'])
    
    print(f"\n[문자열 예시 2]")
    print(f"입력: {ex['input']}")
    print(f"예상: {ex['expected_output']}")
    print(f"결과: {result}")
    
    assert isinstance(result, str), "문자열 입력은 문자열로 반환되어야 함"
    assert '투자신탁으로' in result, "투 자신탁으로 → 투자신탁으로 교정 실패"


def test_all_examples_accuracy(corrector, examples):
    """전체 예시 정확도 테스트"""
    total = len(examples)
    correct = 0
    
    print(f"\n\n{'='*60}")
    print(f"전체 예시 테스트 결과")
    print(f"{'='*60}")
    
    for i, ex in enumerate(examples):
        result = corrector.correct(ex['input'])
        is_correct = (result == ex['expected_output'])
        
        if is_correct:
            correct += 1
            status = "✓"
        else:
            status = "✗"
        
        print(f"{status} 예시 {i+1} ({ex['id']}): {is_correct}")
        
        if not is_correct:
            print(f"  예상: {ex['expected_output'][:50]}...")
            print(f"  결과: {result[:50]}...")
    
    accuracy = correct / total
    print(f"\n정확도: {correct}/{total} = {accuracy:.1%}")
    print(f"{'='*60}")
    
    # 60% 이상이면 통과
    assert accuracy >= 0.6, f"전체 정확도가 60% 미만입니다: {accuracy:.1%}"


if __name__ == "__main__":
    # 직접 실행 시
    pytest.main([__file__, "-v", "-s"])
