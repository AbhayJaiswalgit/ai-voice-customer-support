from langchain_classic.agents import create_react_agent,AgentExecutor
from app.agent.lc_tools import (
    search_products_tool,
    product_details_tool,
    product_faq_tool,
    track_order_tool,
    return_check_tool,
    cancel_order_tool,
    policy_tool,
    product_policy_tool
)
from app.agent.llm_provider import llm
from langchain_core.prompts import PromptTemplate


TOOLS = [
    search_products_tool,
    product_details_tool,
    product_faq_tool,
    track_order_tool,
    return_check_tool,
    cancel_order_tool,
    policy_tool,
    product_policy_tool
]

from langchain_core.prompts import PromptTemplate

# Official ReAct format that Mistral can follow
# Updated prompt with Reasoning Checklist integration
# react_agent.py

# ... (keep your imports)

# template = """Answer the following questions as best you can. You have access to the following tools:

# {tools}

# REASONING RULES (STRICT):
# 1. **Multi-Part Analysis**: Before choosing an action, identify all components of the user's request (e.g., if they ask for Return AND Cancel policies, note both).
# 2. **Exhaustive Tool Use**: Do not provide a Final Answer until every component identified in the analysis is addressed.
# 3. **Verification**: Before giving the Final Answer, verify: "Does this answer every part of the original question?"
# 4. **Identity Awareness**: Look for the 'User (ID: XXXX)' prefix in the Question. Use this specific ID (e.g., C0025) as the 'customer_id' argument for all order-related tool calls (tracking, returns, cancellations).

# To use a tool, you MUST use the following format:

# Thought: [Identify all parts of the query. Plan tool calls for each.]
# Action: the action to take, should be one of [{tool_names}]
# Action Input: {{"arg1": "value1", "arg2": "value2"}}
# Observation: the result of the action
# ... (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I have addressed all parts of the user's request.
# Final Answer: the comprehensive final answer to the original input question

# IMPORTANT: Output the Action and Action Input on separate lines.
# IMPORTANT: All 'Action Input' values must be valid JSON objects. Never use plain text for the input.

# Begin!

# Question: {input}
# Thought:{agent_scratchpad}"""

# react_agent.py  -> replace your existing `template = """..."""` block with this

template = """
You are an AI customer support agent for an e-commerce platform.

You MUST follow the ReAct reasoning format strictly.

You have access to the following tools:

{tools}

FORMAT YOU MUST FOLLOW:

Thought: reason about the user request
Action: the tool to use, must be one of [{tool_names}]
Action Input: the input to the tool (plain text, NOT JSON)
Observation: the result from the tool

(You can repeat Thought/Action/Action Input/Observation multiple times)

When you have enough information:

Thought: I have enough information to answer.
Final Answer: your spoken response to the user.

IMPORTANT RULES:

- If the user is greeting or small talk, DO NOT use any tool.
  In that case, directly write:
  Thought: No tool needed.
  Final Answer: <response>

- Tool names must be written EXACTLY as provided.
  Do not add backslashes, quotes, or extra words.

- Action Input must contain ONLY the required text.
  No explanations. No sentences.

- If the Observation from a tool already satisfies the user request,
  you MUST immediately produce:
  Thought: I have enough information to answer.
  Final Answer: ...

- Do NOT plan future steps.
- Do NOT suggest calling other tools unless the user explicitly asks.

- For order tools, Action Input must ONLY be the order id like: O0001

- If the user asks about:
    • product details → use product_details_tool
    • product FAQs → use product_faq_tool
    • product returnability or warranty → use product_policy_tool
    • company return/refund/delivery policy → use policy_tool
    • searching/suggesting products → use search_products_tool



Begin!

Question: {input}

Thought:{agent_scratchpad}
"""


# ... (keep the rest of your agent initialization)

PROMPT = PromptTemplate.from_template(template)


agent = create_react_agent(
    llm=llm,
    tools=TOOLS,
    prompt=PROMPT
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=TOOLS,
    verbose=True,
    max_iterations=7,
    handle_parsing_errors=True
)
