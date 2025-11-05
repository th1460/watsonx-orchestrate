from ibm_watsonx_orchestrate.agent_builder.agents import Agent, AgentKind, AgentStyle

agent = Agent(
    name="CEP_Agent",
    kind=AgentKind.NATIVE,
    llm="watsonx/meta-llama/llama-3-405b-instruct",
    style=AgentStyle.DEFAULT,
    description="A CEP Agent",
    instructions="You are a cep agent created for return informations about zipcode. When the user asks for example 'information about the cep', run the tool consulta_cep",
    tools=["consulta_cep"]
)
