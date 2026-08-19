from langchain_core.tools import tool
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver
from tools.utils import create_file, read_file, read_workspace, update_file
from langchain_core.messages import SystemMessage

memory = MemorySaver()
config = {"configurable": {"thread_id" : "1"}}

class State(TypedDict):
    messages : Annotated[list, add_messages]


llm = ChatOpenAI(
    model = "gpt-4.1-mini",
    temperature = 0.8
)

DESIGN_PATH = "workspace"

@tool
def rewrite(query: str, file: str):
    """Replaces the entire existing project's design details which include hld.md, lld.md, requirements.txt with a new version.

    only use this tool when significant changes to the project's methodolgy and
    logic for the whole application.

    This tool deletes the previous contents of file chosen before writing
    the new version.

    Do NOT use this tool for small additions.
    Use append() for incremental updates.
    Use update() for updation of specific sections of design.md

    Args:
        file: either hld.md, lld.md, requirements.txt
        query:The complete replacement project design.

    Returns:
        Confirmation that the plan was replaced.
    """
    file = os.path.normpath(file)
    full_path = os.path.join(DESIGN_PATH, file)
    if not full_path.exists():
        return f"{file} does not exist, use create to initialize {file}."
    full_path.write_text(query, encoding = "utf-8")
    return f"{file} rewritten successfully."


@tool
def summarize_design(file: str):
    """Use this tool to acquire a quick summary of the design from hld.md, lld.md, requirements.txt file 
            incase of confusions

    Args:
        file: the file name you want the summary of which can be from hld.md, lld.md, requirements.txt.
    Returns:
        a summary of design.md file
    """
    file = os.path.normpath(file)
    full_path = os.path.joinpath(DESIGN_PATH, file)
    if not full_path.exists():
        return f"{file}  does not exist, use  create to  initialize {file}."

    design = DESIGN_PATH.read_text(encoding = "utf-8")
    prompt = f"""
    Summarize the following:
    {design}
    """    

    response = llm.invoke(prompt)
    return response['messages'][-1].content


design_tools = [create_file, rewrite, summarize_design, update_file, read_file]

designer = llm.bind_tools(tools = design_tools)

def designing_agent(state:State):
    response = designer.invoke(state["messages"])
    return {"messages": [response]}

graph_builder = StateGraph(State)

graph_builder.add_node("Designer",  designing_agent)
graph_builder.add_node("tools", ToolNode(tools = design_tools))

graph_builder.add_edge(START, "Designer")
graph_builder.add_conditional_edges(
    "Designer",
    tools_condition
)
graph_builder.add_edge("tools", "Designer")

designer_agent = graph_builder.compile(memory)

prompt = "You are the designing agent for the software, you have to create hld.md -> containing high level design of the application, lld.md -> containing  the low level design of the application, and requirements.txt which inform the user about the modules and libraries used and should be used as pip install requirements.txt. The file hld.md, lld.md, requirements.txt should only be created after you have read or summarized the plan.md of the application (plan file name: plan.md, in workspace/artifacts). If hld.md, lld.md, requirements.txt are already created then ignore the above instructions and only rewrite the design files if the user explicitly states the need for it."

def designing(state:State):
    messages = [
            SystemMessage(content=prompt),
            *state["messages"]
        ]
    
    response = designer_agent.invoke({"messages": messages})
    
    return {"messages": [response["messages"][-1]]}