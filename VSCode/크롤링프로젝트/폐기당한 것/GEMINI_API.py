import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def call_gemini(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_content(chunks):
    joined = "\n".join(chunks)

    return f"""
다음은 대한민국 국회 국방위원회 회의록 일부이다.
정치적 수사는 모두 제거하고, 국방 연구과제·기술·결정사항 및 외국과의 기술 계약 중심으로 요약하라.

요약 조건:
- 핵심 쟁점 3~5개
- 국방 연구과제·기술·결정사항 및 외국과의 기술 계약 관련 내용 우선
- 추측이나 해석 금지

회의록:
{joined}
"""

print(os.getenv("GEMINI_API_KEY"))