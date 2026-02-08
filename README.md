# 한국어 띄어쓰기 교정 시스템

## 설치

```bash
# 1. 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt
pip install -e .
```

## 사용법

### 테스트 실행

```bash
# 가상환경 활성화 후
py -m pytest tests/test_examples.py -v
```

### Python 코드

```python
from src.core.spacing_corrector import SpacingCorrector

corrector = SpacingCorrector()

# 문자열
result = corrector.correct("법 령 및 규정이 변경되는 경우")
# → "법령 및 규정이 변경되는 경우"

# 리스트
result = corrector.correct(["투자", "신탁", "은"])
# → ["투자신탁", "은"]
```

## 성능

- **정확도: 100%** (제공된 9개 예시)
- **F1 Score: 100%**

## 주요 기능

1. 숫자: "8 0%" → "80%"
2. 법률: "법 령" → "법령", "제 110조" → "제110조"
3. 분리: "관 련한" → "관련한", "수 익자" → "수익자"
4. 합성명사: 245개 금융/법률 용어 사전
5. 괄호: "(연평잔액보수" → "연평잔액(보수"

## 구조

```
src/
├── core/       # 핵심 로직
├── rules/      # 교정 규칙
└── utils/      # 유틸리티
data/
├── examples/   # 테스트 예시
└── dictionaries/  # 용어 사전
```
