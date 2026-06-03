from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from ai_agent import graph, SYSTEM_PROMPT, parse_response
from tools import call_emergency

app = FastAPI()


class Query(BaseModel):
    message: str   # <-- 4 spaces before this line


@app.post("/ask")
async def ask(query: Query):

    user_message = query.message.lower()

    suicide_keywords = [
        "suicide",
        "kill myself",
        "end my life",
        "want to die",
        "self harm",
        "i want to suicide"
    ]

    if any(keyword in user_message for keyword in suicide_keywords):
        call_emergency()

        return {
            "response": "I'm really sorry you're feeling this way. I've contacted emergency support to help you.",
            "tool_called": "emergency_call_tool"
        }

    inputs = {
        "messages": [
            ("system", SYSTEM_PROMPT),
            ("user", query.message)
        ]
    }

    stream = graph.stream(inputs, stream_mode="updates")
    tool_called_name, final_response = parse_response(stream)

    return {
        "response": final_response,
        "tool_called": tool_called_name
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)