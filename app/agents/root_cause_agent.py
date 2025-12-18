import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class RootCauseAgent:
    def __init__(self, prompt_path: str):
        # 1. Gemini API 설정
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")
        
        # 설정 로드(초기화)
        genai.configure(api_key=api_key)
        
        # 모델 이름 앞에 'models/'를 명시적으로 붙여서 404 방지
        self.model = genai.GenerativeModel('gemini-2.5-flash') # "gemini-2.5-pro"

        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompt_template = f.read()

    def analyze(self, equipment_id: str, process_type: str, alarm_message: str) -> list:
        # 2. 프롬프트 완성
        prompt = self.prompt_template.format(
            equipment_id=equipment_id,
            process_type=process_type,
            alarm_message=alarm_message
        )

        # 콘텐츠 생성
        response = self.model.generate_content(prompt)

        try:
            content = response.text
            
            # JSON만 추출하는 로직
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
        except Exception as e:
            print(f"Parsing Error: {e}")
            return [{"error": "분석 실패", "raw": response.text}]

# 사용 예시
if __name__ == "__main__":
    # 환경변수에 키가 설정되어 있어야 함: export GEMINI_API_KEY='your_key'
    agent = RootCauseAgent("prompts/root_cause_v1.txt")
    result = agent.analyze(
        equipment_id="CNC-001",
        process_type="정밀 가공",
        alarm_message="Overload Error - Spindle Motor"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))