import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# 에이전트들 불러오기
from agents.root_cause_agent import RootCauseAgent
from agents.retrieval_agent import RetrievalAgent
from agents.action_agent import ActionAgent

# 설정 로드
load_dotenv()

# 페이지 설정
st.set_page_config(page_title="제조 설비 이상 분석 AI", layout="wide")

st.title("🛠️ 제조 설비 이상 분석 에이전트 서비스")
st.markdown("설비 알람 정보를 입력하면 AI가 원인 분석부터 조치 방안까지 제공합니다.")

# 에이전트 초기화 (캐시 처리하여 속도 향상)
@st.cache_resource
def init_agents():
    root_agent = RootCauseAgent("prompts/root_cause_v1.txt")
    retrieval_agent = RetrievalAgent("data/case.json")
    action_agent = ActionAgent()
    return root_agent, retrieval_agent, action_agent

root_agent, retrieval_agent, action_agent = init_agents()

# 사이드바: 데이터 확인
st.sidebar.header("설정 및 데이터")
if st.sidebar.button("최근 알람 로그 불러오기"):
    df = pd.read_csv("data/alarms.csv")
    st.sidebar.dataframe(df.tail(5))

# 메인 화면: 입력 폼
with st.form("alarm_input_form"):
    st.subheader("알람 정보 입력")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        eq_id = st.selectbox("설비 ID", ["CNC-01", "INJ-01", "INJ-02", "PUMP-01"])
    with col2:
        proc_type = st.selectbox("공정 유형", ["Machining", "Injection", "Cooling"])
    with col3:
        alarm_msg = st.text_input("알람 메시지", placeholder="예: Spindle vibration detected")
        
    submit_button = st.form_submit_button("분석 시작")

# 분석 실행 및 결과 출력
if submit_button:
    if not alarm_msg:
        st.error("알람 메시지를 입력해주세요.")
    else:
        with st.spinner("AI 에이전트들이 협업하여 분석 중입니다..."):
            # 1. Root Cause Analysis
            causes = root_agent.analyze(eq_id, proc_type, alarm_msg)
            
            # 2. Similar Case Retrieval
            search_query = causes[0].get('search_keyword', alarm_msg)
            similar_cases = retrieval_agent.search_similar_cases(search_query)
            
            # 3. Action Recommendation
            final_report = action_agent.generate_recommendation(causes, similar_cases)

        # 결과 레이아웃 구성
        st.divider()
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("🔍 1. 원인 분석 결과")
            for cause in causes:
                with st.expander(f"우선순위 {cause.get('priority', 1)}: {cause.get('search_keyword')}"):
                    st.write(cause.get('cause'))
        
        with c2:
            st.subheader("📚 2. 과거 유사 사례")
            if similar_cases:
                for case in similar_cases:
                    st.info(f"**과거 알람:** {case.get('alarm_code')}\n\n**원인:** {case.get('root_cause')}\n\n**조치:** {case.get('action')}")
            else:
                st.write("유사 사례가 발견되지 않았습니다.")

        st.subheader("📋 3. AI 최종 권고 조치 가이드")
        st.success(final_report)