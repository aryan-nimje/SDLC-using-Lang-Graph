from langchain_core.tools import tool
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model = "gpt-4.1-mini",
    temperature = 0.1
)

TEST_RESULTS = "workspace\artifacts\test_results.md"
TEST_PATH = "workspace\artifacts\test.md"
FOLDER_PATH = "workspace"

@tool
def read_workspace(folder: str = "workspace"):
    """
        Use this function when you want to read the workspace, about which files/folder are present in the workspace and which are not.
        Args:
            If workspace is to be read, DO NOT PASS any arguments,
            If a specific folder is to read in  workspace, PASS IN the name of said folder as argument
        Returns:
            names of files present in the workspace with their extensions.
    """
    print(f"Reading {folder}.......")
    if os.path.exists(folder):
        contents = os.listdir(folder)
        print(f"Directory read succesfully.")
    else:
        return "No such directory exists"
    return contents

@tool
def critique_file(file: str):
    """
        USE THIS TOOL on every file present in the workspace to check if the contents of the file are correct and working well
        DO NOT  check files present in artifacts folder present in the workspace.
        
        Args:
            file: the path of the file you want to check
                Ex: \backend\config\database.js
        Returns:
            Confirmation that the file has been critiquied
    """
    full_path = os.path.join(FOLDER_PATH, file)

    with open(TEST_PATH, "r") as f:
        test = f.read()

    with open(full_path, "r") as f:
        content = f.read()

    with open(TEST_RESULTS, "r") as f:
        results = f.read()

    print(f"Critiquing {file}.......")
    prompt = f"""
    These are the test parameters:
    {test}

    These are the current test_results:
    {results}

    Check the below content and whether it passes the test, Only check for specific tests,
    do no apply tests of authentication on an html file only check for test that are related to the content:
    {content}

    Now return the updated test results in form of string with either tick mark on the ones that are cleared 
    or just marked as "passed" after the test and if a test is failed then write a strict one line solution after the test
    and mark it as solution and leave the rest of the contents of test results as they are only update the test section concerned
    with the contents.
    """

    response = llm.invoke(prompt)

    print(f"Critiquing Complete for {file}")
  
    with open(TEST_RESULTS, "w") as f:
        f.write(response)
    print("Test results updated successfully.")

    return "Test results updates in workspace\artifacts\test_results.txt successfuly."


    

    

    

    

    
    

