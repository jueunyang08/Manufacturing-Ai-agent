import os
import pandas as pd
from dotenv import load_dotenv
from agents.root_cause_agent import RootCauseAgent
from agents.retrieval_agent import RetrievalAgent
from agents.action_agent import ActionAgent

load_dotenv()

def main():
    # 0. 준비: 환경 변수 확인 (직접 입력도 가능하지만 보안상 환경변수 권장)
    if not os.getenv("GEMINI_API_KEY"):
        print("에러: GEMINI_API_KEY가 설정되지 않았습니다.")
        return

    # 에이전트 초기화
    root_agent = RootCauseAgent("prompts/root_cause_v1.txt")
    retrieval_agent = RetrievalAgent("data/case.json")
    action_agent = ActionAgent()

    # 1. 최신 알람 데이터 가져오기 (alarms.csv의 마지막 줄)
    df = pd.read_csv("data/alarms.csv")
    latest_alarm = df.iloc[-1]
    
    print(f"\n[1] 새로운 알람 감지: {latest_alarm['alarm_message']} ({latest_alarm['equipment_id']})")

    # 2. Agent 1: 원인 분석
    print("\n[2] Agent 1이 원인을 분석 중입니다...")
    causes = root_agent.analyze(
        equipment_id=latest_alarm['equipment_id'],
        process_type=latest_alarm['process'],
        alarm_message=latest_alarm['alarm_message']
    )
    print(f"분석 결과: {causes}")

    # 3. Agent 2: 유사 사례 검색
    # 가장 높은 확률의 원인(첫 번째 원인)의 키워드로 검색
    search_query = causes[0].get('search_keyword', latest_alarm['alarm_message'])
    print(f"\n[3] Agent 2가 '{search_query}' 키워드로 과거 사례를 찾는 중...")
    similar_cases = retrieval_agent.search_similar_cases(search_query)
    print(f"검색된 사례: {similar_cases}")

    # 4. Agent 3: 조치 권고안 생성
    print("\n[4] Agent 3이 최종 조치 가이드를 작성 중입니다...")
    final_report = action_agent.generate_recommendation(causes, similar_cases)

    # 5. 결과 출력
    print("\n" + "="*50)
    print("최종 분석 보고서")
    print("="*50)
    print(final_report)
    print("="*50)

if __name__ == "__main__":
    main()