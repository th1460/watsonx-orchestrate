from ibm_watsonx_orchestrate.agent_builder.agents import Agent, AgentKind, AgentStyle

agent = Agent(
    name="Query_Agent",
    kind=AgentKind.NATIVE,
    llm="watsonx/meta-llama/llama-3-405b-instruct",
    style=AgentStyle.DEFAULT,
    description="A Query Agent",
    instructions="You are a query agent created for query data. When the user asks for example 'count a column from table', run the query data flow OR when the user ask for report you should execute generate report flow",
    tools=["query_data_flow", "generate_report"]
)
