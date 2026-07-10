"""
TrafficVision AI
Dashboard Module

Creates Plotly charts for the Streamlit dashboard.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


class Dashboard:

    def __init__(self):
        pass

    def vehicle_distribution_chart(self, class_counts):
        """
        Creates a Pie Chart showing vehicle distribution.
        """
        labels = list(class_counts.keys())
        values = list(class_counts.values())

        fig = px.pie(
            names=labels,
            values=values,
            title="Vehicle Distribution",
            hole=0.45
        )

        fig.update_layout(
            template="plotly_dark",
            height=420
        )

        return fig

    def vehicle_bar_chart(self, class_counts):
        """
        Creates vehicle count bar chart.
        """
        df = pd.DataFrame({
            "Vehicle": list(class_counts.keys()),
            "Count": list(class_counts.values())
        })

        fig = px.bar(
            df,
            x="Vehicle",
            y="Count",
            text="Count",
            title="Vehicle Count"
        )

        fig.update_layout(
            template="plotly_dark",
            height=420
        )

        return fig

    def traffic_trend_chart(self, history):
        """
        Draws live traffic trend.
        """
        if len(history) == 0:
            history = [0]

        frames = list(range(len(history)))

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=frames,
                y=history,
                mode="lines+markers",
                name="Traffic"
            )
        )

        fig.update_layout(
            title="Traffic Trend",
            xaxis_title="Frame",
            yaxis_title="Vehicles",
            template="plotly_dark",
            height=420
        )

        return fig

    def density_gauge(self, density):
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=density,
                domain={'x': [0.08, 0.92], 'y': [0, 1]},  # keep the gauge centered within its container
                title={"text": "Traffic Density (%)", "font": {"size": 16}},
                number={
                    "font": {"size": 28},   # fixed size so Plotly can't auto-scale it into the arc
                    "valueformat": ".0f",   # whole-number display
                    "suffix": "%",
                },
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "limegreen"},
                    "steps": [
                        {"range": [0, 40], "color": "green"},
                        {"range": [40, 70], "color": "orange"},
                        {"range": [70, 100], "color": "red"},
                    ],
                },
            )
        )

        fig.update_layout(
            template="plotly_dark",
            height=280,                          # reduced height to prevent vertical stretching
            margin=dict(l=15, r=15, t=40, b=15),  # tight margins so number has room without waste
            autosize=True
        )

        return fig

    def metrics(self, total, cars, bikes, buses, trucks):
        return {
            "Total": total,
            "Cars": cars,
            "Motorcycles": bikes,
            "Buses": buses,
            "Trucks": trucks
        }