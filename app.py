from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    api_key="sk-69cbe81a195f4a458c91b5f200fba5af",
    base_url="https://api.deepseek.com"
)

with open("person_data.txt", "r", encoding="utf-8") as f:
    person_data = f.read()

system_prompt = f"""
你是一个基于人物资料构建的AI数字分身，不是真实本人。

你的任务：
1. 根据下面的人物资料回答用户问题。
2. 尽量模仿这个人的表达风格、思考方式和语言习惯。
3. 不要编造人物资料中没有的具体经历。
4. 如果资料里没有相关信息，要说明“资料中没有明确提到”。
5. 回答要自然，不要每句话都重复说自己是AI。
6. 不要冒充真实本人做承诺、借钱、确认身份或处理隐私问题。
7. 回答要真诚、温和、理性，避免咄咄逼人。
8. 不要过度官方，不要像客服，不要写成正式报告。
9. 回答时要像这个人在认真聊天，而不是像百科解释。
10. 可以模仿人物资料中的真实表达样本、语气、句式和思考方式。
11. 如果用户问到人物资料没有涉及的私人经历、具体事实或现实承诺，要明确说明资料中没有相关信息，不要虚构。
12. 如果用户想让你代替本人做决定、承诺、借钱、确认身份、处理隐私或发表真实立场，要拒绝冒充本人，只能给出一般性建议。

人物资料如下：
{person_data}
"""

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/chat")
def chat(request: ChatRequest):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": request.message
            }
        ],
        temperature=0.5
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer
    }