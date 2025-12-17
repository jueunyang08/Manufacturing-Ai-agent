# AI Agent Role Design

## Agent 1: Root Cause Analysis Agent
역할:
- 제조 설비 알람 로그를 해석하여
- 발생 가능한 원인을 추론한다.

입력:
- 설비 ID
- 공정 유형
- 알람 메시지

출력:
- 가능 원인 목록 (중요도 순)

판단 기준:
- 알람 메시지의 키워드
- 공정 유형별 일반적인 고장 패턴

## Agent 2: Similar Case Retrieval Agent
역할:
- Agent 1에서 도출된 원인을 기반으로
- 과거 유사 사례를 검색한다.

입력:
- 원인 키워드

출력:
- 과거 사례 (원인 / 조치 / 예방)

기술:
- Vector Embedding 기반 유사도 검색

## Agent 3: Action Recommendation Agent
역할:
- 현재 알람과 과거 사례를 종합하여
- 즉시 조치 및 재발 방지 대책을 생성한다.

입력:
- 원인 분석 결과
- 유사 사례 정보

출력:
- 즉시 조치
- 장기 예방 대책

