# Watson Orchestrate ADK

## Setup

```bash
# Read environment variables
source .env

# Adding an environment
orchestrate env add --name my-orchestrate --url $WOX_URL --type ibm_iam

# Activate
orchestrate env activate my-orchestrate --api-key $WOX_API_KEY

# Starting your ADK project
mkdir -p adk-project/{agents,tools,knowledge}

adk-project
├── agents
│   └── query_agent.py
├── knowledge
└── tools
    ├── markdown_format.py
    ├── query_data_flow.py
    └── query_data.py

# Set connection
orchestrate connections add -a cos_connection
orchestrate connections configure -a cos_connection --env live --kind key_value --type team
orchestrate connections set-credentials -a cos_connection -k key_value --env live \
-e S3_REGION=$S3_REGION \
-e S3_ENDPOINT=$S3_ENDPOINT \
-e S3_ACCESS_KEY_ID=$S3_ACCESS_KEY_ID$ \
-e S3_SECRET_ACCESS_KEY=$S3_SECRET_ACCESS_KEY

# Create flow
orchestrate tools import -k flow -p adk-project/tools/ -f adk-project/tools/query_data_flow.py

# Create tools
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
orchestrate tools import -k python -f adk-project/tools/query_data.py -a cos_connection -r requirements.txt
orchestrate tools import -k python -f adk-project/tools/markdown_format.py -r requirements.txt

# Create agent
orchestrate agents import -f adk-project/agents/query_agent.py
```