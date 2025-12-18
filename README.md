# Manufacturing-Ai-agent
LLM-based AI agent service for analyzing manufacturing equipment alarms and generating actionable insights

제조 설비에서 발생하는 이상 알람을 분석하여
원인 추정 및 조치 가이드를 제공하는 AI Agent 서비스

## Problem
제조 현장에서는 설비 알람 발생 시
원인 분석과 대응이 작업자 경험에 의존하여
조치 시간이 지연되는 문제가 있다.

## Solution
본 프로젝트는 LLM 기반 AI Agent를 활용하여
설비 알람 로그를 분석하고
과거 사례를 기반으로 조치 가이드를 자동 생성한다.

1.분석: LLM이 알람 로그의 기술적 의미를 해석합니다.
2.검색: Vector DB(RAG)를 통해 과거 수리 이력 중 유사 사례를 찾아냅니다.
3.추천: 분석 결과와 과거 사례를 종합하여 즉시 조치 및 재발 방지 대책을 생성합니다.

## Architecture
Alarm Input
 → Root Cause Analysis Agent
 → Similar Case Retrieval
 → Action Recommendation Agent

## AI Agent Design
- Root Cause Analysis Agent: 알람 원인 추론
- Similar Case Retrieval Agent: 과거 사례 검색
- Action Recommendation Agent: 조치 가이드 생성

## Tech Stack
anguage: Python 3.10+
AI 모델 (LLM): Google Gemini 1.5 Flash (Generative AI)
AI 프레임워크: Google Generative AI SDK
Vector Database (RAG): ChromaDB (임베딩 및 유사도 검색용)
Frontend/UI: Streamlit (Python-based Web Framework)
Data Management: Pandas (CSV 처리), JSON
Environment: python-dotenv (보안 및 환경 설정)
Architecture: Multi-Agent System (분석 - 검색 - 생성 3단계 구조)

## How to Run
pip install -r requirements.txt
streamlit run app/ui_app.py

## Limitations & Future Work
- 실제 MES 연동은 Mock 데이터 기반
- 실시간 스트리밍 처리 미구현
- 향후 ERP/MES 연동 가능
