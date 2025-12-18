import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class ActionAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_recommendation(self, causes, similar_cases):
        prompt = f"""
        당신은 제조 설비 수리 전문가입니다. 
        아래의 분석된 원인과 과거 사례를 참고하여 작업자에게 줄 '최종 조치 가이드'를 작성하세요.

        1. 분석된 원인: {causes}
        2. 과거 유사 사례: {similar_cases}

        형식:
        - [즉시 조치 사항]: (현장에서 바로 할 일)
        - [장기 예방 대책]: (다시 발생하지 않게 할 일)
        - [주의 사항]: (작업 시 위험 요소 등)
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    