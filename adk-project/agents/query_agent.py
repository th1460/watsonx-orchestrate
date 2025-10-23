from ibm_watsonx_orchestrate.agent_builder.agents import Agent, AgentKind, AgentStyle

agent = Agent(
    name="Query_Agent",
    kind=AgentKind.NATIVE,
    llm="watsonx/meta-llama/llama-3-405b-instruct",
    style=AgentStyle.DEFAULT,
    description="A Query Agent",
    instructions="You are a query agent created for query data. When the user asks 'query my data', run the query data tool",
    collaborators=[],
    tools=["query_data_count"]  
    )
