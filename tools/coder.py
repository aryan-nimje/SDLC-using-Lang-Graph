from langchain_core.tools import tool
from pathlib import Path
import os
from langchain_openai import ChatOpenAI
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver
from tools.tester import testing

memory = MemorySaver()
config = {"configurable": {"thread_id" : "1"}}

class State(TypedDict):
    messages : Annotated[list, add_messages]

llm = ChatOpenAI(
    model = "gpt-4.1-mini",
    temperature = 0.1
    )

FOLDER_PATH = "workspace"

@tool
def create_file(file: str, code: str):
    """
    This tool initializes a file into the workspace.

    Use this tool when, the user's prompt indicates to creating a project file,

    DO NOT USE this tool when you need to update any file use update instead.

    There is no limit to making files. You may make any number of files as long 
    as it satisfies the user's request just  make sure they are well structured and dont have 
    similar named  and are integrated perfectly

    Args: 
        file: a string input which contains to parts, first the file name and second the
                the extension of file. The variable should be passed in format of:
                    name.extension
                    where name.extension is the file created and written the code into
            Ex: name.html -> for html  file
                name.js -> for javascript file
                name.css -> for css file
                name.c -> for c file
                name.cpp -> for c plus plus file
                name.py -> for python file
        
        code: a string input which contains the implementation of user's request/prompt.

    Returns:
        Confirmation about file created.
    """
    os.makedirs(FOLDER_PATH, exist_ok=True)

    file = os.path.normpath(file)
    full_path = os.path.join(FOLDER_PATH, file)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    print(f"Writing code into {full_path}......")

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Code succesfully written into {full_path}")

    return f"code written in {file} successfully."

@tool
def update_file(file: str, query: str):
    """
    This tool updates a file/section of a in the workspace.

    Use this tool when, the user's prompt indicates to updating or adding
    some new features or implementation into a project file,

    DO NOT USE this tool when you need to create a file use create instead.

    Args: 
        file: a string input which contains to parts, first the file name and second the
                the extension of file. The variable should be passed in format of:
                    name.extension
                    where name.extension file is the file needed to be updated.
            Ex: name.html -> for html  file
                name.js -> for javascript file
                name.css -> for css file
                name.c -> for c file
                name.cpp -> for c plus plus file
                name.py -> for python file
        
        query: a string input which precisely concludes what and how the user wants to update 
                in the file.

    Returns:
        Confirmation about file updated.
    """
    full_path = os.path.join(FOLDER_PATH, file)
    print(f"Updating {file}......")

    with open(full_path, "r") as f:
        contents = f.read()

    updated = llm.invoke(
    f"""
    You are editing an existing source file.

    Return ONLY the complete updated file contents.
    Do not use markdown.
    Do not wrap the code in ``` fences.

    Current file:
    {contents}

    Requested change:
    {query}
    """
    )

    with open(full_path, "w") as f:
        f.write(updated.content)

    print(f"File {file} updated sucesfully.")
    return f"File {file} updated successfully."

@tool
def read_workspace():
    """
        Use this function when you want to read the workspace, about which files are present in the workspace and which are not.

        Returns:
            names of files present in the workspace with their extensions.
    """
    folder = "workspace"
    return os.listdir(folder)
        
@tool
def read_file(file:str):
    """
        This tool returns the contents of a specific file present in the workspace. Can be used  to remember content of a certain
        file and also while making more that are dependent on a specific file.
        For example: linking multiple webapages in .html file

        Args:
            file: a string input which contains two parts, first the file name and second the
                the extension of file. The variable should be passed in format of:
                name.extension
                where name.extension is the file which has its content read.
                Ex: name.html -> for html  file
                name.js -> for javascript file
                name.css -> for css file
                name.c -> for c file
                name.cpp -> for c plus plus file
                name.py -> for python file
        Returns:
            The content of the specified file
    """
    full_path = os.path.join(FOLDER_PATH, file)

    if not os.path.isfile(full_path):
        return "No such file found in the workspace. Use create to initialize the file if needed."

    with open(full_path, "r") as f:
        content = f.read()

    return content

coder_tools = [create_file, read_file, read_workspace, update_file, testing]

coder = llm.bind_tools(tools = coder_tools)

def coding_agent(state:State):
    response = coder.invoke(state["messages"])
    return {"messages": [response]}

graph_builder = StateGraph(State)

graph_builder.add_node("Coder",  coding_agent)
graph_builder.add_node("tools", ToolNode(tools = coder_tools))

graph_builder.add_edge(START, "Coder")
graph_builder.add_conditional_edges(
    "Coder",
    tools_condition
)
graph_builder.add_edge("tools", "Coder")

designer = graph_builder.compile(memory)

def designing(state:State):
    response = designer.invoke(state["messages"])
    return response["messages"][-1].content





    

    

