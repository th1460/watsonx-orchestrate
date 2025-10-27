from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pandas import DataFrame


@tool(permission=ToolPermission.READ_ONLY)
def markdown_format(df: list[tuple]) -> str:
    """Executes the tool's action based on the provided input.

    Args:
        df (list[tuple]): List of tuples.

    Returns:
        str: Query results in markdown format.
    """

    return DataFrame(df, columns=["Variable", "N", "%"]).to_markdown(index=False)
