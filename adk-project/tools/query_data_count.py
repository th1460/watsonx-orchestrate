from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.agent_builder.connections import ExpectedCredentials, ConnectionType
from ibm_watsonx_orchestrate.run import connections
import duckdb

APP_ID = "cos_connection"

@tool(permission=ToolPermission.READ_ONLY,
      expected_credentials=[
        ExpectedCredentials(
            app_id = APP_ID,
            type=ConnectionType.KEY_VALUE
        )
    ])
def query_data_count(table: str, column: str) -> str:
    """Executes the tool's action based on the provided input.

    Args:
        table (str): Table
        column (str): Column

    Returns:
        str: Query results
    """

    creds = connections.key_value(APP_ID)


    with duckdb.connect("/tmp/db.duckdb") as con:
        con.execute(
                f"""
                SET home_directory='/tmp';
                INSTALL httpfs;
                LOAD httpfs;
                CREATE SECRET (
                TYPE S3,
                KEY_ID '{creds.get("S3_ACCESS_KEY_ID")}',
                SECRET '{creds.get("S3_SECRET_ACCESS_KEY")}',
                REGION '{creds.get("S3_REGION")}',
                ENDPOINT '{creds.get("S3_ENDPOINT")}'
                );
                CREATE OR REPLACE TABLE titanic AS
                SELECT *
                FROM read_csv('s3://wox-tables/titanic.csv');
                """
                )

        res = con.execute(
                f"""
                SELECT {column}, COUNT({column}) AS N FROM {table} GROUP BY {column};
                """
                ).fetch_df().to_markdown(index=False)

    return res
