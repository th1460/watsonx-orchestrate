from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.agent_builder.connections import ExpectedCredentials, ConnectionType
from ibm_watsonx_orchestrate.run import connections
from htmltools import TagList, Tag, HTMLDependency, HTML
from htmltools.tags import body, div, script
from upload_cos import upload_cos
import duckdb

APP_ID = "cos_connection"


@tool(permission=ToolPermission.ADMIN,
      expected_credentials=[
          ExpectedCredentials(
              app_id=APP_ID,
              type=ConnectionType.KEY_VALUE
          )])
def generate_report(report_name: str) -> str:
    """Executes the tool's action based on the provided input.

    Args:
        report_name (str): Report name

    Returns:
        str: Report generated.
    """

    themes_dep = HTMLDependency(
        name="themes",
        version="1.0",
        source={
            "href": "https://1.www.s81c.com/common/carbon/web-components/version/v2.11.1"
        },
        stylesheet={"href": "themes.css"},
    )

    plex_dep = HTMLDependency(
        name="plex",
        version="1.0",
        source={
            "href": "https://1.www.s81c.com/common/carbon-for-ibm-dotcom/version/v2.11.1"
        },
        stylesheet={"href": "plex.css"},
    )

    grid_dep = HTMLDependency(
        name="grid",
        version="1.0",
        source={
            "href": "https://1.www.s81c.com/common/carbon/web-components/version/v2.11.1"
        },
        stylesheet={"href": "grid.css"},
    )

    ui_shell_dep = HTMLDependency(
        name="ui-shell",
        version="1.0",
        source={
            "href": "https://1.www.s81c.com/common/carbon/web-components/version/v2.11.1",
        },
        script={
            "type": "module",
            "src": "ui-shell.min.js",
        },
    )

    ui_shell = Tag(
        "cds-header",
        {"aria-label": "Titanic Report"},
        Tag("cds-header-name", {"href": "", "prefix": "Titanic"}, "Report"),
    )

    chart_dep = HTMLDependency(
        name="charts",
        version="1.0",
        source={"href": "https://unpkg.com/@carbon/charts@latest/dist"},
        script={
            "src": "umd/bundle.umd.js",
        },
        stylesheet={"href": "styles.css"},
    )

    def simple_bar_chart(id, data, value, group, title):
        page = TagList(
            chart_dep.as_html_tags(),
            plex_dep.as_html_tags(),
            div(id=id, style="width: 100%; height: 100%"),
            script(
                HTML(
                    """
                    new Charts.SimpleBarChart(document.getElementById('%s'), {
                            data: %s,
                            options: {
                        theme: 'white',
                        title: '%s',
                        axes: {
                            left: {
                                mapsTo: '%s',
                                scaleType: 'labels',
                                truncation: {
                                    type: 'none',
                                }
                            },
                            bottom: {
                                mapsTo: '%s',
                            }
                        },
                        legend: {position: 'right',
                            orientation: 'vertical',
                            truncation: {type: 'none'}
                            },
                        height: '300px',
                        width: '600px'
                        }
                        })
                        """
                    % (id, data, title, group, value)
                )
            ),
        )
        return page

    creds = connections.key_value(APP_ID)

    with duckdb.connect("/tmp/db.duckdb") as con:
        con.execute(
            f"""
            SET home_directory='/tmp';
            INSTALL httpfs;
            LOAD httpfs;
            CREATE SECRET (
            TYPE S3,
            KEY_ID '{creds.get("S3_ACCESS_KEY_ID_READ")}',
            SECRET '{creds.get("S3_SECRET_ACCESS_KEY_READ")}',
            REGION '{creds.get("S3_REGION")}',
            ENDPOINT '{creds.get("S3_ENDPOINT")}'
            );
            CREATE OR REPLACE TABLE titanic AS
            SELECT *
            FROM read_csv('s3://wox-tables/titanic.csv',
                types = ['VARCHAR', 'VARCHAR', 'VARCHAR']);
            """
        )

        df1 = con.execute(
            """
            SELECT Sex AS group,
            COUNT(Sex) AS N,
            round(100 * N/SUM(N) OVER (), 1) AS '%'
            FROM titanic
            GROUP BY Sex;
            """
        ).fetch_df().to_dict(orient="records")

        df2 = con.execute(
            """
            SELECT Pclass AS group,
            COUNT(Pclass) AS N,
            round(100 * N/SUM(N) OVER (), 1) AS '%'
            FROM titanic
            GROUP BY Pclass;
            """
        ).fetch_df().to_dict(orient="records")

        df3 = con.execute(
            """
            SELECT Survived AS group,
            COUNT(Survived) AS N,
            round(100 * N/SUM(N) OVER (), 1) AS '%'
            FROM titanic
            GROUP BY Survived;
            """
        ).fetch_df().to_dict(orient="records")

    page = TagList(
        ui_shell_dep,
        themes_dep,
        grid_dep,
        plex_dep,
        body(class_="cds-theme-zone-white"),
        ui_shell,
        div(
            div(
                TagList(
                    div(
                        simple_bar_chart("plot1", df1, "%", "group", "Frequency Sex"),
                        class_="cds--col",
                    ),
                    div(
                        simple_bar_chart("plot3", df3, "%", "group", "Frequency Survived"),
                        class_="cds--col",
                    ),
                ),
                class_="cds--row",
                style="margin-top:5rem",
            ),
            div(
                TagList(
                    div(
                        simple_bar_chart("plot2", df2, "%", "group", "Frequency Pclass"),
                        class_="cds--col",
                    ),
                    div(
                        class_="cds--col",
                    ),
                ),
                class_="cds--row",
                style="margin-top:5rem",
            ),
            class_="cds--grid",
        ),
    )
    page.save_html("/tmp/index.html")
    with open("/tmp/index.html", 'r', encoding="utf-8") as file:
        html_content = file.read()

    output = upload_cos(str(html_content).encode("utf-8"), creds)

    return output
