from langchain_core.tools import tool

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
    

@tool
def create(text:str):
    """Creates a new project planning document (plan.txt)

    Use this tool only when no plan exists.
    This tool initializes the project planning document that all later SDLC agents refer to.

    Do not use  when plan already exists use rewrite or append.
    Args:
        text: a thorough input that maps out the goals, risks and methodology for project developement
    Returns:
        confirmation that  the plan.txt file is initialized.
    """

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

@tool
def read_plan():
    """ Use this when the planner has to understand current project state  before choosing  between append, rewrite and create

    Returns:
        the current project plan.
    """

@tool 
def summarize_plan():
    """Use this to summarize the plan if the plan gets too long or is inefficient to read_plan()
    Returns:
        Summary of plan file(plan.txt).
    """
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