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
    temperature = 0.6
)

ARTIFACTS_PATH = "workspace/artifacts"

@tool
def append(query: str, file: str):
    """Appends new information to the project plan or test without modifying or removing the existing content.

        Use this tool when project plan or test already exists and new goals, requirements, risks, assumptions, milestones or 
        implementation details or test parameters need to be added

        Do Not Use this tool when existing sections of plan or test need to be modified or removed, Use update instead.
    Args:
        query: an input that will be appended onto the plan leaving the rest untouched.
        file: either plan.md incase of adding goals, acheivements, risks, milestones etc. 
                or test.md incase of additions to testing parameters
    Returns:
        confirmation that the new query was succesfully appended onto plan.
    """
    file = os.path.normpath(file)
    full_path = os.path.join(ARTIFACTS_PATH, file)
    if not full_path.exists():
        return f"{file} does not exist, use create_file to initialize {file}."
    with open(full_path, "a") as f:
        f.write("\n\n")
        f.write(query)
    return "query appended succesfully/"

@tool
def rewrite(query: str, file: str):
    """Replaces the entire existing project plan  or test with a new version.

    Use this tool when significant changes to the project's goals,
    scope, requirements, architecture, or implementation strategy
    make the existing plan  or the test obsolete.

    This tool deletes the previous contents of plan.md and test.md before writing
    the new version.

    Do NOT use this tool for small additions.
    Use append() for incremental updates.

    Args:
        query:The complete replacement project plan in case of rewriting plan.md or testing process  in case of rewriting test.md.
        file: a string input either plan.md or test.md

    Returns:
        Confirmation that the plan was replaced.
    """
    os.makedirs(ARTIFACTS_PATH, exist_ok=True)
    
    file = os.path.normpath(file)
    full_path = os.path.join(ARTIFACTS_PATH, file)
    
    print(f"Rewriting {file}......")
    with open(full_path, "w") as f:
        f.write(query)
        print(f"Successfully written into {file}.")
    return f"Text successfully rewritten into {file}."


def summarize(file: str):
    """Use this tool to acquire a quick summary of the plan from plan.md or test parameters from test.md file incase of confusions

    Returns:
        a summary of plan.md file
    """
    file = os.path.normpath(file)
    full_path = os.path.join(ARTIFACTS_PATH, file)
    if not full_path.exists():
        return f"{file} does not exist, use  create_file to  initialize {file}"

    plan = full_path.read_text(encoding = "utf-8")
    prompt = f"""
    Summarize the following:
    {plan}
    """    
    return llm.invoke(prompt).content

plan_tools = [update_file, create_file, append, rewrite, read_file, summarize, read_workspace]

planner = llm.bind_tools(tools = plan_tools)

def planning_agent(state:State):
    response = planner.invoke(state["messages"])
    return {"messages": [response]}

graph_builder = StateGraph(State)

graph_builder.add_node("Planner",  planning_agent)
graph_builder.add_node("tools", ToolNode(tools = plan_tools))

graph_builder.add_edge(START, "Planner")
graph_builder.add_conditional_edges(
    "Planner",
    tools_condition
)
graph_builder.add_edge("tools", "Planner")

planner_agent = graph_builder.compile(memory)

system_prompt = "You are the planning agent for this application: You need to initialize two files, plan.md and test.md if not already initialized, plan.md contains the goals, acheivements, milestones, potential risks and all that matters in planning of application. test.md contains the test parameters as the tester of the application being built. The application description goes as: "

def planning(state: State):
    messages = [
        SystemMessage(content=system_prompt),
        *state["messages"]
    ]

    response = planner_agent.invoke({"messages": messages})

    return {"messages": [response["messages"][-1]]}

