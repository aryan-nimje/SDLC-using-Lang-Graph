from langchain_core.tools import tool
from pathlib import Path
import os
from langchain_openai import ChatOpenAI

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

    REMEMBER while using this tool to create plan.md, test.md, hld.md, lld.md and requirements.md the file string should  be:
        file : artifact/file.extension
        where file may be plan, text, hld, lld, requirements and extensions may be either md or txt

    There is no limit to making files. You may make any number of files as long 
    as it satisfies the user's request just  make sure they are well structured and dont have 
    similar names  and are integrated perfectly

    Args: 
        file:  a string input which contains to parts, first the file name and second the
                the extension of file. And while using this tool to create plan.md, test.md, hld.md, lld.md and requirements.md 
                the file string should  be: artifacts/file.extension. The variable should be passed in format of:
                name.extension
                where name.extension is the file created and written the code into
            Ex: name.html -> for html  file
                name.js -> for javascript file
                name.css -> for css file
                name.c -> for c file
                name.cpp -> for c plus plus file
                name.py -> for python file
                name.md -> for makdown file
                name.txt -> for text file
        
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
def read_file(file:str):
    """
        This tool returns the contents of a specific file present in the workspace. Can be used  to remember content of a certain
        file and also while making more that are dependent on a specific file.
        For example: linking multiple webapages in .html file

        Args:
            file: a string input which contains two parts, first the file name and second the
                the extension of file. And while using this tool to access plan.md, test.md, hld.md, lld.md and requirements.md 
                the file argument should  be: artifacts\file.extension. The variable should be passed in format of:
                name.extension
                where name.extension is the file which has its content read.
                Ex: name.html -> for html  file
                name.js -> for javascript file
                name.css -> for css file
                name.c -> for c file
                name.cpp -> for c plus plus file
                name.py -> for python file
                name.md -> for  markdown file
                name.txt -> for text file
        Returns:
            The content of the specified file
    """
    full_path = os.path.join(FOLDER_PATH, file)

    if not os.path.isfile(full_path):
        return "No such file found in the workspace. Use create to initialize the file if needed."

    with open(full_path, "r") as f:
        content = f.read()

    return content

def read_workspace():
    """
        Use this function when you want to read the workspace, about which files are present in the workspace and which are not.

        Returns:
            names of files present in the workspace with their extensions.
    """
    folder = "workspace"
    return os.listdir(folder)
