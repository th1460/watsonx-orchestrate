from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
import requests


@tool(permission=ToolPermission.READ_ONLY)
def consulta_cep(cep: str) -> dict:
    """Executes the tool's action based on the provided input.

    Args:
        cep (str): Zipcode.

    Returns:
        dict: Return information about the code inserted.
    """
    url = f"https://viacep.com.br/ws/{cep}/json/"
    res = requests.get(url)
    res = res.json()
    return res
