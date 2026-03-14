import os
import streamlit as st
import anthropic

SYSTEM_PROMPT = """당신은 교육학 분야의 최고 전문가이자 논문 작성 멘토입니다. 특히 교육학 논문 작성에 깊은 전문성을 갖추고 있습니다.

## 핵심 전문 영역

### 1. 교육학 논문 작성 (최우선 전문 분야)

**연구 설계**
- 연구 문제(Research Question) 및 연구 목적 진술 방법
- 연구 가설 설정 (귀무가설, 연구가설)
- 변인 설정 (독립변인, 종속변인, 매개변인, 조절변인)
- 연구의 필요성 및 의의 작성법

**연구 방법론**
- 양적 연구: 실험연구, 준실험연구, 조사연구, 상관연구
- 질적 연구: 현상학, 근거이론, 문화기술지, 사례연구, 내러티브 탐구
- 혼합연구: 수렴적 설계, 설명적 순차 설계, 탐색적 순차 설계
- 연구 방법 선택 기준 및 타당성 논증

**문헌 고찰**
- 체계적 문헌 고찰 방법
- 선행연구 분석 및 비판적 검토
- 이론적 배경 구성 방법
- 연구의 차별성과 독창성 부각

**연구 도구 및 측정**
- 설문지 개발 및 타당도·신뢰도 검증 (내용타당도, 구인타당도, 공인타당도)
- Cronbach's α, 확인적 요인분석(CFA)
- 관찰도구, 면담 프로토콜 개발
- 루브릭 및 수행평가 도구 설계

**자료 분석**
- 양적 분석: t검정, ANOVA, ANCOVA, 회귀분석, 구조방정식(SEM), 위계적 회귀
- 질적 분석: 주제분석, 내용분석, 개방코딩·축코딩·선택코딩
- 혼합연구 분석: 통합 및 연결 전략

**논문 각 섹션 작성**
- 서론: 연구 배경→문제 제기→연구 목적→연구 문제→용어 정의 흐름
- 이론적 배경: 개념 정의→이론 고찰→선행연구 분석→시사점 도출
- 연구 방법: 연구 설계→연구 대상→연구 도구→자료 수집→분석 방법
- 연구 결과: 연구 문제별 결과 제시, 표·그림 활용
- 논의: 결과 해석→선행연구 비교→시사점→제한점
- 결론: 요약→교육적 함의→후속연구 제언

**논문 형식**
- APA 7판 인용 및 참고문헌 형식
- KCI(한국학술지인용색인) 등재 학술지 형식
- 학위논문(석사·박사) 형식
- 교육부/한국연구재단 보고서 형식

### 2. 교육과정 설계
- 백워드 설계(UbD), ADDIE, Dick & Carey 모델
- Bloom의 신·구 분류학, Marzano 분류학
- 역량 중심 교육과정, 2022 개정 교육과정
- 교수학습 지도안 작성

### 3. 학습 이론
- 행동주의, 인지주의, 구성주의, 연결주의
- Vygotsky ZPD, Piaget 인지발달, Bruner 발견학습
- 자기조절학습, 메타인지, 정보처리이론
- 동기이론 (SDT, 기대-가치이론, 귀인이론)

## 응답 원칙
- 논문 작성 요청 시 **실제로 쓸 수 있는 문장**을 직접 작성해줍니다.
- 학술적 표현과 교육학 전문 용어를 정확하게 사용합니다.
- 피드백 요청 시 구체적인 수정 방향과 개선된 문장을 함께 제시합니다.
- APA 7판 기준으로 인용 형식을 안내합니다.
- 한국 교육 맥락(국가교육과정, 교육부 정책, KCI 학술지 기준)을 반영합니다.
- 답변은 논문에 바로 활용할 수 있도록 체계적으로 제시합니다."""

PAPER_TEMPLATES = {
    "📌 연구 문제 설정": "제 논문 주제는 '{주제}'입니다. 이 주제로 적절한 연구 문제(Research Question) 3개와 연구 가설을 작성해주세요. 연구 문제는 교육학 논문 형식에 맞게 구체적으로 진술해주세요.",
    "📖 서론 작성": "'{주제}' 관련 교육학 논문의 서론을 작성해주세요. 연구 배경, 연구의 필요성, 연구 목적, 연구 문제, 용어 정의 순서로 구성해주세요.",
    "📚 문헌 고찰 구성": "'{주제}' 논문의 이론적 배경 및 문헌 고찰 목차를 구성해주고, 각 항목에서 다뤄야 할 핵심 내용과 주요 학자/이론을 안내해주세요.",
    "🔬 연구 방법 선택": "'{주제}'를 연구하려 합니다. 양적/질적/혼합 연구 중 어떤 방법이 적합한지 근거와 함께 추천해주고, 구체적인 연구 설계 방법을 알려주세요.",
    "📊 연구 결과 기술": "다음 연구 결과를 교육학 논문 형식에 맞게 기술해주세요: {결과 내용}. 표나 수치 해석 방법도 포함해주세요.",
    "💬 논의 작성": "'{연구 결과}'가 나왔습니다. 이 결과에 대한 논의 섹션을 작성해주세요. 선행연구와의 비교, 교육적 시사점, 연구의 제한점을 포함해주세요.",
    "✍️ 초록 작성": "다음 내용을 바탕으로 교육학 논문 초록(국문/영문)을 작성해주세요: 연구 목적: {목적}, 방법: {방법}, 결과: {결과}",
    "🔗 APA 참고문헌": "다음 자료들을 APA 7판 형식으로 참고문헌 목록을 작성해주세요: {자료 정보}",
    "✅ 논문 피드백": "다음 논문 내용을 검토하고 학술적 표현, 논리 구조, 교육학적 적절성 측면에서 구체적인 피드백과 수정 문장을 제시해주세요:\n\n{논문 내용}",
    "📋 연구 계획서": "'{주제}'로 교육학 연구 계획서를 작성해주세요. 연구 필요성, 연구 목적, 연구 문제, 연구 방법, 기대 효과를 포함해주세요.",
}

st.set_page_config(
    page_title="교육학 전문 Claude",
    page_icon="🎓",
    layout="wide"
)

if "api_key" not in st.session_state:
    st.session_state.api_key = os.environ.get("ANTHROPIC_API_KEY", "")

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
    if st.button("대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.markdown("**일반 빠른 질문**")
    general_questions = [
        "UbD 모델로 단원 계획 짜는 법",
        "Vygotsky ZPD 이론 설명",
        "Bloom 분류학 학습목표 작성",
        "자기조절학습 전략 종류",
        "2022 개정 교육과정 핵심역량",
    ]
    for q in general_questions:
        if st.button(q, use_container_width=True, key=f"gen_{q}"):
            st.session_state.pending_question = q
            st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

tab1, tab2 = st.tabs(["💬 대화", "📝 논문 작성 도우미"])

with tab2:
    st.markdown("### 논문 섹션별 작성 도우미")
    st.caption("버튼을 클릭하면 해당 섹션 작성을 위한 프롬프트가 대화창에 입력됩니다. 괄호 안의 내용을 본인 연구에 맞게 수정해서 사용하세요.")
    st.markdown("")

    cols = st.columns(2)
    for i, (label, template) in enumerate(PAPER_TEMPLATES.items()):
        with cols[i % 2]:
            if st.button(label, use_container_width=True, key=f"paper_{label}"):
                st.session_state.pending_question = template
                st.session_state.active_tab = "chat"
                st.rerun()

    st.divider()
    st.markdown("### 논문 작성 가이드")
    with st.expander("📌 교육학 논문 기본 구조"):
        st.markdown("""
**학술지 논문 구조**
1. 제목 / 저자 / 소속
2. 국문초록 + 핵심어 (5개 내외)
3. 서론 (연구 배경, 필요성, 목적, 문제)
4. 이론적 배경 (개념 정의, 선행연구)
5. 연구 방법 (설계, 대상, 도구, 절차, 분석)
6. 연구 결과 (연구 문제별 제시)
7. 논의 및 결론 (해석, 시사점, 제한점, 제언)
8. 참고문헌
9. 영문초록 + Keywords
        """)
    with st.expander("📌 APA 7판 인용 형식"):
        st.markdown("""
**본문 인용**
- 저자 1인: (홍길동, 2023) 또는 홍길동(2023)
- 저자 2인: (홍길동 & 김철수, 2023)
- 저자 3인 이상: (홍길동 et al., 2023)

**참고문헌**
- 학술지: 홍길동. (2023). 논문제목. *학술지명*, *권*(호), 시작쪽-끝쪽. https://doi.org/...
- 단행본: 홍길동. (2023). *책제목*. 출판사.
- 학위논문: 홍길동. (2023). *논문제목* [박사학위논문, 대학교명].
        """)
    with st.expander("📌 연구 방법론 선택 기준"):
        st.markdown("""
**양적 연구** → 가설 검증, 변인 간 관계, 일반화
- 실험연구: 처치 효과 검증
- 조사연구: 현황 파악, 관계 분석

**질적 연구** → 의미 탐색, 경험 이해, 맥락 파악
- 현상학: 경험의 본질 탐구
- 근거이론: 이론 생성
- 사례연구: 특정 사례 심층 분석

**혼합연구** → 양적+질적 상호보완
- 설명적 순차: 양적→질적으로 설명
- 탐색적 순차: 질적→양적으로 검증
        """)

with tab1:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if "pending_question" in st.session_state:
        prompt = st.session_state.pop("pending_question")
    else:
        prompt = st.chat_input("교육학 관련 질문을 입력하세요...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            client = anthropic.Anthropic(api_key=api_key)
            response_placeholder = st.empty()
            full_response = ""

            with client.messages.stream(
                model="claude-opus-4-6",
                max_tokens=8192,
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
