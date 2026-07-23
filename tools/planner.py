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

PLAN_PATH = Path("workspace/plan.md")

@tool
def append(query: str):
    """Appends new information to the project plan without modifying or removing the existing content.

        Use this tool when project plan already exists and new goals, requirements, risks, assumptions, milestones or implementation details need to be added

        Do Not Use this tool when existing sections of plan need to be modified or removed, Use rewrite instead.
    Args:
        query: an input that will be appended onto the plan leaving the rest untouched.
    Returns:
        confirmation that the new query was succesfully appended onto plan.
    """
    if not PLAN_PATH.exists():
        return "plan.md does not exist, use create to initialize plan.md"
    with open(PLAN_PATH, "a") as f:
        f.write("\n\n")
        f.write(query)
    return "query appended succesfully/"

@tool
def create(text:str):
    """Creates a new project planning document (plan.md)

    Use this tool only when no plan exists.
    This tool initializes the project planning document that all later SDLC agents refer to.

    Do not use  when plan already exists use rewrite or append.
    Args:
        text: a thorough input that maps out the goals, risks and methodology for project developement
    Returns:
        confirmation that  the plan.txt file is initialized.
    """
    PLAN_PATH.parent.mkdir(parents=True, exist_ok=True)

    if PLAN_PATH.exists():
        return "plan.md already exists, use rewrite, update or append tools"
    PLAN_PATH.write_text(text, encoding = "utf-8")
    return "plan.md created successfully."

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
