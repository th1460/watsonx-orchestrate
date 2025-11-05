from pydantic import BaseModel
from ibm_watsonx_orchestrate.flow_builder.flows import END, Flow, flow, START
from .query_data import query_data
from .markdown_format import markdown_format


class InputData(BaseModel):
    """
    This class represents a input data.

    Attributes:
        table (str): Table.
        column (str): Column.
    """
    table: str
    column: str


class QueryResults(BaseModel):
    results: str


@flow(name="query_data_flow",
      input_schema=InputData,
      output_schema=QueryResults)
def query_data_flow(aflow: Flow = None) -> Flow:
    """
    Creates a flow with two tools: query_data and markdown_format.
    This flow will rely on the Flow engine to perform automatic data mapping at runtime.
    Always see the knowledge database to get the correct column.
    The correct column is prefixed with column='correct column name', always use the 'correct column name',
    get the correct column name more similar to the description. Examples: 'query column from table'
    Args:
        flow (Flow, optional): The flow to be built. Defaults to None.
    Returns:
        Flow: The created flow.
    """

    query_data_node = aflow.tool(query_data)
    markdown_format_node = aflow.tool(markdown_format, output_schema=QueryResults)

    aflow.sequence(START, query_data_node, markdown_format_node, END)

    return aflow
