import os
import streamlit as st
import anthropic

SYSTEM_PROMPT = """당신은 교육학 전문 AI 어시스턴트입니다. 다음 세 가지 핵심 영역에서 깊은 전문성을 갖추고 있습니다:

1. **교육과정 설계 (Curriculum Design)**
   - 백워드 설계(Backward Design), UbD(Understanding by Design) 등 교육과정 설계 모델
   - 학습목표 진술 (Bloom의 분류학, ABCD 공식 등)
   - 교육과정 재구성, 성취기준 분석, 단원/차시 계획 작성
   - 역량 중심 교육과정, 통합 교육과정 설계

2. **학습 이론 (Learning Theory)**
   - 행동주의 (Pavlov, Skinner), 인지주의 (Piaget, Vygotsky), 구성주의 학습이론
   - 정보처리이론, 메타인지, 자기조절학습
   - 동기이론 (자기결정이론, 기대-가치이론, Maslow, Herzberg)
   - 사회학습이론, 상황학습이론, 연결주의
   - 뇌기반 학습, 개별화 학습(UDL)

3. **교육학 논문 작성 지원**
   - APA/KCI 논문 형식, 인용 방법
   - 연구 방법론 (질적·양적·혼합 연구)
   - 문헌 고찰 작성, 연구 문제 및 가설 설정
   - 연구 결과 해석, 논의 및 결론 작성
   - 교육학 주요 학술지 논문 스타일 안내

**응답 원칙:**
- 교육학 전문 용어를 정확하게 사용하되, 필요시 쉽게 설명합니다.
- 이론과 실제를 연결하여 실용적인 도움을 제공합니다.
- 논문 작성 지원 시 학술적 엄밀성을 유지합니다.
- 한국 교육 맥락(국가교육과정, 교육부 정책 등)을 고려합니다.
- 답변은 체계적이고 구조적으로 제시합니다."""

st.set_page_config(
    page_title="교육학 전문 Claude",
    page_icon="🎓",
    layout="wide"
)

# API Key 초기화
if "api_key" not in st.session_state:
    st.session_state.api_key = os.environ.get("ANTHROPIC_API_KEY", "")

# API Key 입력 화면
if not st.session_state.api_key:
    st.title("🎓 교육학 전문 Claude")
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔑 API Key 입력")
        st.markdown("Anthropic API Key를 입력해주세요.")
        key_input = st.text_input(
            "API Key",
            type="password",
            placeholder="sk-ant-...",
            label_visibility="collapsed"
        )
        if st.button("시작하기", use_container_width=True, type="primary"):
            if key_input.startswith("sk-ant-"):
                st.session_state.api_key = key_input
                st.rerun()
            else:
                st.error("올바른 API Key 형식이 아닙니다. (sk-ant-로 시작)")
        st.markdown("")
        st.caption("API Key는 [console.anthropic.com](https://console.anthropic.com/settings/api-keys) 에서 발급받을 수 있습니다.")
    st.stop()

api_key = st.session_state.api_key

st.title("🎓 교육학 전문 Claude")
st.caption("교육과정 설계 · 학습 이론 · 논문 작성 전문 AI 어시스턴트")

with st.sidebar:
    st.header("설정")
    st.success("API Key 연결됨 ✓")
    if st.button("API Key 변경", use_container_width=True):
        st.session_state.api_key = ""
        st.rerun()
    st.divider()
    st.markdown("**전문 분야**")
    st.markdown("- 📚 교육과정 설계")
    st.markdown("- 🧠 학습 이론")
    st.markdown("- 📝 교육학 논문 작성")
    st.divider()
    if st.button("대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.markdown("**빠른 질문 예시**")
    example_questions = [
        "UbD 모델로 단원 계획 짜는 법",
        "Vygotsky ZPD 이론 설명",
        "논문 연구방법론 선택 기준",
        "Bloom 분류학 학습목표 작성",
        "자기조절학습 전략 종류",
    ]
    for q in example_questions:
        if st.button(q, use_container_width=True, key=q):
            st.session_state.pending_question = q
            st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if "pending_question" in st.session_state:
    prompt = st.session_state.pop("pending_question")
else:
    prompt = st.chat_input("교육학 관련 질문을 입력하세요...")

if prompt:
    if not api_key:
        st.error("사이드바에서 Anthropic API Key를 입력해주세요.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        client = anthropic.Anthropic(api_key=api_key)
        response_placeholder = st.empty()
        full_response = ""

        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            thinking={"type": "adaptive"},
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
