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

memory = MemorySaver()
config = {"configurable": {"thread_id" : "1"}}

class State(TypedDict):
    messages : Annotated[list, add_messages]

llm = ChatOpenAI(
    model = "gpt-4.1-mini",
    temperature = 0.8
)

ARTIFACTS_PATH = "workspace/artifacts"

@tool
def append(query: str):
    """Appends new information to the project plan or test without modifying or removing the existing content.

        Use this tool when project plan or test already exists and new goals, requirements, risks, assumptions, milestones or 
        implementation details or test parameters need to be added

        Do Not Use this tool when existing sections of plan or test need to be modified or removed, Use update instead.
    Args:
        query: an input that will be appended onto the plan leaving the rest untouched.
    Returns:
        confirmation that the new query was succesfully appended onto plan.
    """
    if not ARTIFACTS_PATH.exists():
        return "plan.md or does not exist, use create to initialize plan.md"
    with open(ARTIFACTS_PATH, "a") as f:
        f.write("\n\n")
        f.write(query)
    return "query appended succesfully/"

@tool
def create(text:str, file: str):
    """Creates a new project document (plan.md or test.txt)

    Use this tool only when no plan and no test document exists.
    This tool initializes the project planning document that all later SDLC agents refer to.

    Do not use  when plan already exists use rewrite or append.
    Args:
        text: a thorough input that maps out the goals, risks and methodology for project developement in case of plan.md,
                and a through input stating the test parameters for the application which it should pass which may be technical
                and logical.
        file: a string input either plan.md or test.md
    Returns:
        confirmation that the plan.md or test.md file is initialized.
    """
    os.makedirs(ARTIFACTS_PATH, exist_ok=True)

    file = os.path.normpath(file)
    full_path = os.path.join(ARTIFACTS_PATH, file)

    print(f"Creating {file}......")
    with open(full_path, "w") as f:
        f.write(text)
        print(f"Successfully written into {file}.")
    return f"Text successfully written into {file}."


@tool
def rewrite(query: str):
    """Replaces the entire existing project plan with a new version.

    Use this tool when significant changes to the project's goals,
    scope, requirements, architecture, or implementation strategy
    make the existing plan obsolete.

    This tool deletes the previous contents of plan.txt before writing
    the new version.

    Do NOT use this tool for small additions.
    Use append() for incremental updates.

    Args:
        query:The complete replacement project plan.

    Returns:
        Confirmation that the plan was replaced.
    """
    if not PLAN_PATH.exists():
        return "plan.md does not exist, use create to initialize plan.md"
    PLAN_PATH.write_text(query, encoding = "utf-8")
    return "plan.md rewritten successfully."


@tool
def read_plan():
    """ Use this when the planner has to understand current project state  before choosing  between append, rewrite and create

    Returns:
        the current project plan.
    """
    if not PLAN_PATH.exists():
         return "plan.md does not exist, use create to initialize plan.md"
    return PLAN_PATH.read_text(encoding = "utf-8")

def summarize_plan():
    """Use this tool to acquire a quick summary of the plan from plan.md file incase of confusions

    Returns:
        a summary of plan.md file
    """
    if not PLAN_PATH.exists():
        return "plan.md  does not exist, use  create to  initialize plan.md."

    plan = PLAN_PATH.read_text(encoding = "utf-8")
    prompt = f"""
    Summarize the following:
    {plan}
    """    
    return llm.invoke(prompt).content

@tool
def update_plan(instruction: str):
    """
    Updates only the relevant portions of the existing project plan while
    preserving all unrelated content.

    Use this tool when specific sections of the project plan need to be
    modified, corrected, or replaced without rewriting the entire document.

    Do NOT use this tool for adding entirely new information (use append)
    or replacing the entire plan (use rewrite).

    Args:
        instruction: A description of the desired modification.

    Returns:
        Confirmation that the requested changes were applied.
    """
    if not PLAN_PATH.exists():
            return "plan.md  does not exist, use  create to  initialize plan.md."

    plan = PLAN_PATH.read_text(encoding= "utf-8")

    prompt = f"""
    Current plan:
    {plan}

    Instructions:
    {instruction}

    Rewrite only the necessary sections of plan and preserve everything else."""
    
    updated_plan = llm.invoke(prompt)

    PLAN_PATH.write_text(updated_plan.content, encoding= "utf-8")
    return "plan.md updated succesfully."

plan_tools = [update_plan, create, append, rewrite, read_plan, summarize_plan]

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

planner = graph_builder.compile(memory)

def planning(state:State):
    response = planner.invoke(state["messages"])
    return response["messages"][-1].content


