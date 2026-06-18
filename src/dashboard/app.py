from dash import Dash, html, dcc
import plotly.express as px

from src.analytics.drg_analytics import DRGAnalytics
from src.ingestion.provider_loader import ProviderLoader
from src.ingestion.ipps_loader import IPPSLoader
from src.transform.merger import DRGMerger
from src.transform.revenue_metrics import RevenueMetrics

app = Dash(__name__)


provider_df = ProviderLoader(
    "data/Medicare_IP_Hospitals_by_Provider_and_Service_2024.csv"
).load()

ipps_df = IPPSLoader("data/CMS-1833-F Table 5.xlsx").load()

merged_df = DRGMerger().merge(
    provider_df,
    ipps_df,
)

final_df = RevenueMetrics().add_metrics(
    merged_df,
)

total_revenue = final_df["Total_Revenue"].sum()

total_discharges = final_df["Tot_Dschrgs"].sum()

top_revenue_df = DRGAnalytics().top_revenue_drgs(
    final_df,
)

top_volume_df = DRGAnalytics().top_volume_drgs(
    final_df,
)

top_revenue_df["Rank"] = range(
    1,
    len(top_revenue_df) + 1,
)

ranking_df = top_revenue_df.copy()

top_revenue_df = top_revenue_df.sort_values(
    "Total_Revenue",
    ascending=True,
)

chart_df = top_revenue_df.copy()

chart_df["Chart_Row"] = [str(i) for i in range(len(chart_df))]

revenue_fig = px.bar(
    chart_df,
    x="Total_Revenue",
    y="Chart_Row",
    orientation="h",
    title="Top Revenue DRGs",
)

revenue_fig.update_layout(
    paper_bgcolor="#020B2D",
    plot_bgcolor="#020B2D",
    font_color="#00D4FF",
    title_font_size=24,
    xaxis_title="Revenue ($)",
    yaxis_title="",
    height=700,
)

revenue_fig.update_yaxes(
    visible=False,
)

revenue_fig.update_traces(
    customdata=chart_df[["DRG_Desc"]],
    hovertemplate="<b>%{customdata[0]}</b><br>" "Revenue: $%{x:,.0f}" "<extra></extra>",
    marker_color="#00D4FF",
    width=0.75,
)

volume_fig = px.bar(
    top_volume_df,
    x="Tot_Dschrgs",
    y="DRG_Desc",
    orientation="h",
    title="Top Volume DRGs",
)

volume_fig.update_layout(
    paper_bgcolor="#020B2D",
    plot_bgcolor="#020B2D",
    font_color="#00D4FF",
    title_font_size=24,
    height=700,
)

volume_fig.update_traces(
    marker_color="#00D4FF",
    width=0.75,
)


def shorten(text, limit=45):
    if len(text) <= limit:
        return text
    return text[:limit] + "..."


ranking_panel = html.Div(
    [
        html.Div(
            [
                html.H3(
                    f"#{row.Rank}",
                    className="rank-number",
                ),
                html.P(
                    shorten(row.DRG_Desc),
                    className="rank-text",
                ),
            ],
            className="rank-card",
        )
        for _, row in ranking_df.iterrows()
    ],
    style={
        "width": "30%",
        "padding": "20px",
    },
)

app.layout = html.Div(
    [
        html.H1(
            "Healthcare Revenue Intelligence Platform",
            style={
                "color": "#00D4FF",
                "textAlign": "center",
            },
        ),
        html.Hr(),
        html.Div(
            [
                html.Div(
                    [
                        html.H4("Total Revenue"),
                        html.H2(f"${total_revenue:,.0f}"),
                    ],
                    className="kpi-card",
                ),
                html.Div(
                    [
                        html.H4("Total Discharges"),
                        html.H2(f"{total_discharges:,.0f}"),
                    ],
                    className="kpi-card",
                ),
                html.Div(
                    [
                        html.H4("Mapping Rate"),
                        html.H2("98.86%"),
                    ],
                    className="kpi-card",
                ),
            ],
            className="kpi-container",
        ),
        html.Br(),
        html.Div(
            [
                ranking_panel,
                html.Div(
                    [
                        dcc.Graph(
                            figure=revenue_fig,
                        ),
                    ],
                    style={
                        "width": "70%",
                        "border": "1px solid #00D4FF",
                        "borderRadius": "10px",
                        "padding": "10px",
                    },
                ),
            ],
            style={
                "display": "flex",
                "alignItems": "flex-start",
                "marginTop": "20px",
            },
        ),
        html.Br(),
        html.Div(
            [
                dcc.Graph(
                    figure=volume_fig,
                ),
            ],
            style={
                "border": "1px solid #00D4FF",
                "borderRadius": "10px",
                "padding": "10px",
                "marginTop": "20px",
            },
        ),
    ]
)

print(ranking_df[["Rank", "Total_Revenue"]])

if __name__ == "__main__":
    app.run(debug=True)
