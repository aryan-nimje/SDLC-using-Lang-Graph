from langchain_core.tools import tool
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI

#Currently agent acts on it own and does not consider plan.md ir design.md files
#further work will be done to take that into account.

llm = ChatOpenAI(
    model = "gpt-4.1-mini",
    temperature = 0.8
)

FOLDER_PATH = "agent_testing_grounds/workspace"

@tool
def create_file(file: str, code: str):
    """
    This tool initializes a file into the workspace.

    Use this tool when, the user's prompt indicates to creating a project file,

    DO NOT USE this tool when you need to update any file use update  instead.

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

    full_path = os.path.join(FOLDER_PATH, file)

    print(f"Writing code into {full_path}......")
    with open(full_path, "w") as f:
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

    prompt = f"""
    Given this code: {contents}

    Only edit/update parts/sections necessary to: {query}

    and return while preserving other details.
    """

    updated = llm.invoke(prompt)

    with open(full_path, "w") as f:
        f.write(updated['messages'][-1].content)

    print(f"File {file} updated sucesfully.")


    

    

