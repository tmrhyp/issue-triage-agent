from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import list_open_issues, get_issue_body, post_triage_comment
from typing import TypedDict

llm = ChatAnthropic(model="claude-sonnet-4-20250514")
tools = [list_open_issues, get_issue_body, post_triage_comment]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a GitHub issue triage agent. "
               "Classify each issue as bug, feature, or question. "
               "Post a brief triage comment on each. Be concise."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

class State(TypedDict):
    repo: str
    result: str

def triage_node(state: State):
    result = executor.invoke({
        "input": f"Triage all open issues in the repo: {state['repo']}"
    })
    return {"result": result["output"]}

def build_graph():
    g = StateGraph(State)
    g.add_node("triage", triage_node)
    g.set_entry_point("triage")
    g.add_edge("triage", END)
    return g.compile()
