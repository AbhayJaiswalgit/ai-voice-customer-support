import json
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tool_executor import execute_tool
from langchain_core.messages import SystemMessage, HumanMessage

MAX_STEPS = 5  # safety limit

def run_agent(llm, user_message: str, context: dict):

    conversation = SYSTEM_PROMPT + f"\nUser: {user_message}\n"

    for step in range(MAX_STEPS):

        ai_msg = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=conversation)
    ])

        response = ai_msg.content.strip()


        try:
            data = json.loads(response)
        except Exception:
            return "Sorry, I couldn't understand that."

        # ✅ Final answer
        if "final_answer" in data:
            return data["final_answer"]

        # 🔧 Tool request
        if "action" in data:
            tool_name = data["action"]
            args = data.get("arguments", {})

            result = execute_tool(tool_name, args, context)

            # Feed result back to LLM
            conversation += (
                f"Agent Thought: {data.get('thought','')}\n"
                f"Tool Result: {result}\n"
            )
        else:
            return "Sorry, something went wrong."

    return "I couldn't complete the request. Please try again."
