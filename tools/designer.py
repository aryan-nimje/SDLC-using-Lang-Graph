from langchain_core.tools import tool
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model = "gpt-4.1-mini",
    temperature = 0.8

)

DESIGN_PATH = Path("workspace/design.md")

@tool
def create(text:str):
    """Creates a new project designing document (design.md) 

    Use this tool only when no design exists.
    This tool initializes the project designing document that all later SDLC agents refer to.

    Do not use  when design already exists use rewrite or append.
    Args:
        text: a well structured text that defines whether the application will be monolithic or divided into 
            microservices. Informs about the modules/dependencies used in the application development
            and when the application is working, also how these modules are related/connected
            to each other. And finally which database soultion the application will require if required.
            And also how system connects/integrates with external apis or softwares if any used 
    Returns:
        confirmation that the design.md file is initialized.
    """
    DESIGN_PATH.parent.mkdir(parents=True, exist_ok=True)

    if DESIGN_PATH.exists():
        return "design.md already exists, use rewrite, update or append tools"
    DESIGN_PATH.write_text(text, encoding = "utf-8")
    return "design.md created successfully."

@tool
def rewrite(query: str):
    """Replaces the entire existing project design with a new version.

    only use this tool when significant changes to the project's methodolgy and
    logic for the whole application.

    This tool deletes the previous contents of design.txt before writing
    the new version.

    Do NOT use this tool for small additions.
    Use append() for incremental updates.
    Use update() for updation of specific sections of design.md

    Args:
        query:The complete replacement project design.

    Returns:
        Confirmation that the plan was replaced.
    """
    if not DESIGN_PATH.exists():
        return "design.md does not exist, use create to initialize plan.md"
    DESIGN_PATH.write_text(query, encoding = "utf-8")
    return "design.md rewritten successfully."

@tool
def read_design():
    """Use this when the designer has to understand current project state  before choosing  
        between append, rewrite and create

    Returns:
        the current project design.
    """
    if not DESIGN_PATH.exists():
         return "design.md does not exist, use create to initialize design.md"
    return DESIGN_PATH.read_text(encoding = "utf-8")

@tool
def append(query: str):
    """Appends new information to the project design without modifying or removing the existing content.

        Use this tool when project plan already exists and new development logic should be added to better the design.

        Do Not Use this tool when existing sections of plan need to be modified or removed, Use update() instead.
    Args:
        query: an input that will be appended onto the design leaving the rest untouched.
    Returns:
        confirmation that the new query was succesfully appended onto design.md
    """
    if not DESIGN_PATH.exists():
        return "design.md does not exist, use create to initialize plan.md"
    with open(DESIGN_PATH, "a") as f:
        f.write("\n\n")
        f.write(query)
    return "query appended succesfully/"

@tool
def summarize_design():
    """Use this tool to acquire a quick summary of the design from deisgn.md file 
    incase of confusions

    Returns:
        a summary of design.md file
    """
    if not DESIGN_PATH.exists():
        return "design.md  does not exist, use  create to  initialize design.md."

    design = DESIGN_PATH.read_text(encoding = "utf-8")
    prompt = f"""
    Summarize the following:
    {design}
    """    
    return llm.invoke(prompt).content

@tool
def update_design(instruction: str):
    """
    Updates only the relevant portions of the existing project design while
    preserving all unrelated content.

    Use this tool when specific sections of the project design need to be
    modified, corrected, or replaced without rewriting the entire document.

    Do NOT use this tool for adding entirely new information (use append)
    or replacing the entire plan (use rewrite).

    Args:
        instruction: A description of the desired modification.

    Returns:
        Confirmation that the requested changes were applied.
    """
    if not DESIGN_PATH.exists():
        return "design.md  does not exist, use  create to  initialize design.md."

    design = DESIGN_PATH.read_text(encoding= "utf-8")

    prompt = f"""
    Current plan:
    {design}

    Instructions:
    {instruction}

    Rewrite only the necessary sections of plan and preserve everything else."""
    
    updated_plan = llm.invoke(prompt)

    DESIGN_PATH.write_text(updated_plan.content, encoding= "utf-8")
    return "plan.md updated succesfully."

