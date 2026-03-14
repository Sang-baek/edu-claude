# 🎓 교육학 전문 Claude

교육과정 설계, 학습 이론, 교육학 논문 작성을 도와주는 AI 어시스턴트입니다.

## 만든 사람

김상백

## 주요 기능

- 📚 교육과정 설계 (UbD, Bloom 분류학, 성취기준 분석 등)
- 🧠 학습 이론 (Vygotsky, Piaget, 자기조절학습 등)
- 📝 교육학 논문 작성 지원 (APA 형식, 연구방법론 등)

## 실행 방법 1

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```


## 실행 방법 2
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## 자주 발생하는 오류 및 해결 방법

### 1. `streamlit` 명령어를 인식하지 못할 때
```
'streamlit' 용어가 인식되지 않습니다.
```
**해결:** `streamlit` 대신 `python -m streamlit` 사용
```bash
python -m streamlit run app.py
```

---

### 2. `anthropic` 패키지 설치가 안 될 때
```
ERROR: Could not find a version that satisfies the requirement anthropic>=0.40.0 (from versions: none)
```
**원인:** Python 버전이 너무 최신(3.14)이라 패키지 호환이 안 됨

**해결:** Python 3.11 설치 후 사용
1. [python.org/downloads/release/python-3119](https://www.python.org/downloads/release/python-3119/) 에서 Python 3.11 설치
2. 설치 시 **"Add Python to PATH"** 반드시 체크
3. 새 터미널 열고 아래 명령어 실행:
```bash
py -m pip install anthropic streamlit
py -m streamlit run app.py
```

---

### 3. API 크레딧 부족 오류
```
anthropic.BadRequestError: Your credit balance is too low to access the Anthropic API.
```
**원인:** Anthropic API 크레딧이 없음 (Claude Pro 구독과 별개)

**해결:** [console.anthropic.com/settings/billing](https://console.anthropic.com/settings/billing) 에서 크레딧 충전 (최소 $5)

> ⚠️ Claude Pro(claude.ai) 구독은 API와 별개입니다. API 크레딧을 따로 구매해야 합니다.

---

### 4. API Key 발급 방법
[console.anthropic.com/settings/api-keys](https://console.anthropic.com/settings/api-keys) 에서 발급
- Key는 `sk-ant-`로 시작하는 문자열
- 앱 실행 후 첫 화면에서 입력
