from langchain_classic.agents import create_react_agent,AgentExecutor
from app.agent.lc_tools import (
    search_products_tool,
    product_details_tool,
    product_faq_tool,
    track_order_tool,
    return_check_tool,
    policy_tool
)
from app.agent.llm_provider import llm
from langchain_core.prompts import PromptTemplate


TOOLS = [
    search_products_tool,
    product_details_tool,
    product_faq_tool,
    track_order_tool,
    return_check_tool,
    policy_tool
]

from langchain_core.prompts import PromptTemplate

# Official ReAct format that Mistral can follow
# Updated prompt with Reasoning Checklist integration
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

REASONING RULES (STRICT):
1. **Multi-Part Analysis**: Before choosing an action, identify all components of the user's request (e.g., if they ask for Return AND Cancel policies, note both).
2. **Exhaustive Tool Use**: Do not provide a Final Answer until every component identified in the analysis is addressed.
3. **Verification**: Before giving the Final Answer, verify: "Does this answer every part of the original question?"

To use a tool, you MUST use the following format:

Thought: [Identify all parts of the query. Plan tool calls for each.]
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I have addressed all parts of the user's request.
Final Answer: the comprehensive final answer to the original input question

IMPORTANT: Output the Action and Action Input on separate lines.

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

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
    max_iterations=20,
    handle_parsing_errors=True
)
