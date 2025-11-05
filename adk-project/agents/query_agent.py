from ibm_watsonx_orchestrate.agent_builder.agents import Agent, AgentKind, AgentStyle

agent = Agent(
    name="Query_Agent",
    kind=AgentKind.NATIVE,
    llm="watsonx/meta-llama/llama-3-405b-instruct",
    style=AgentStyle.DEFAULT,
    description="A Query Agent",
    instructions="You are a query agent created for query data. When the user asks for example 'query a column from table' or 'count a column from table' should run the query_data_flow. When the user ask for report you should execute generate_report tool. If I ask about the knowledge database, show me this content",
    tools=["query_data_flow", "generate_report"],
    knowledge_base=["database_knowledge"]
)
