# 한국어 띄어쓰기 교정 시스템 - 제출 문서

## 1. 소스 코드

```
src/core/spacing_corrector.py    # 메인 교정 클래스
src/rules/                        # 숫자/법률/합성명사/패턴 규칙
data/dictionaries/                # 245개 금융/법률 용어 사전
tests/test_examples.py            # 테스트
```

## 2. Input/Output 예시

### 빠른 실행

```bash
# 가상환경 활성화 후
py -m pytest tests/test_examples.py -v
```

### 예시 1 (문자열)

```python
input:  "법 령 및 규정이 변경되는 경우"
output: "법령 및 규정이 변경되는 경우"
```

### 예시 2 (배열)

```python
input:  ["투자", "신탁", "은"]
output: ["투자신탁", "은"]
```

### 제공된 9개 예시 결과

| 번호 | 패턴                         | 결과   |
| ---- | ---------------------------- | ------ |
| 1    | 관 련한 → 관련한             | ✓ 정확 |
| 2    | 사 전에 → 사전에             | ✓ 정확 |
| 3    | 수 익자가 → 수익자가         | ✓ 정확 |
| 4    | 비 용 → 비용, 괄호 교정      | ✓ 정확 |
| 5    | 8 0% → 80%                   | ✓ 정확 |
| 6    | 정상 케이스                  | ✓ 정확 |
| 7    | 것으로 서 → 것으로서         | ✓ 정확 |
| 8    | 법 령 → 법령                 | ✓ 정확 |
| 9    | 투 자신탁으로 → 투자신탁으로 | ✓ 정확 |

**정확도: 9/9 (100%)**

## 3. 설명

### 구조

```
[입력] → [전처리] → [규칙 기반 교정] → [후처리] → [출력]
```

### 핵심 기술

1. **규칙 기반**: LLM 런타임 호출 없음, 정규표현식 + 사전
2. **도메인 특화**: 245개 금융/법률 용어 사전
3. **타입 안정성**: 입력 타입 그대로 출력

### 사용법

```python
from src.core.spacing_corrector import SpacingCorrector

corrector = SpacingCorrector()
result = corrector.correct(input_data)
```

## 4. 에러율

### 평가 지표

```
Accuracy:   100.00%
Char F1:    100.00%
Word F1:    100.00%
Precision:  100.00%
Recall:     100.00%
```

### 처리 패턴

- ✅ 숫자: "8 0%" → "80%"
- ✅ 법률: "제 110조" → "제110조"
- ✅ 분리: "관 련한" → "관련한"
- ✅ 합성명사: "투자 신탁" → "투자신탁"
- ✅ 괄호: "(연평잔액보수" → "연평잔액(보수"

**에러율: 0% (9/9 정확)**

## 5. 설치 및 실행

### 설치

```bash
# 1. 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt
pip install -e .
```

### 테스트 실행

```bash
# 가상환경 활성화 (이미 활성화되어 있지 않다면)
venv\Scripts\activate

# 전체 테스트
py -m pytest tests/test_examples.py -v
```

## 6. 라이선스

모든 패키지는 BSD/Apache 라이선스로 상업적 사용 가능
