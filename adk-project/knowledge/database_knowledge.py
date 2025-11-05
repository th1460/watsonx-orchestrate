from ibm_watsonx_orchestrate.agent_builder.knowledge_bases.knowledge_base import KnowledgeBase

knowledge_base = KnowledgeBase(
    name="database_knowledge",
    description="A description of databases",
    documents=["database_knowledge.txt"],
    vector_index={
         "embeddings_model_name": "ibm/slate-125m-english-rtrvr-v2"}
)
