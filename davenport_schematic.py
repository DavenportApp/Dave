import streamlit as st
import plotly.graph_objects as go
import math

def davenport_machine_graphic(station_data=None):
    """
    Draw a Davenport schematic with end- and side-working tools,
    with custom position ordering and angles as specified by user.
    Position mapping (counterclockwise):
    1 = 7 o'clock (220°), 2 = 4 o'clock (320°), 3 = 2 o'clock (50°),
    4 = 12 o'clock (90°), 5 = 10 o'clock (145°)
    """

    labels = ["Pos 1", "Pos 2", "Pos 3", "Pos 4", "Pos 5"]
    center = (0, 0)
    main_radius = 1.1
    outer_radius = 1.7  # Move side tools farther out

    # Angles in degrees for each position, counterclockwise
    angles_deg = [220, 320, 30, 90, 150]
    angles = [math.radians(a) for a in angles_deg]

    positions = [(center[0] + main_radius * math.cos(a),
                  center[1] + main_radius * math.sin(a)) for a in angles]
    side_positions = [(center[0] + outer_radius * math.cos(a),
                      center[1] + outer_radius * math.sin(a)) for a in angles]

    fig = go.Figure()
    # Main machine outline
    fig.add_shape(type="circle", x0=-1.4, y0=-1.4, x1=1.4, y1=1.4,
                  line_color="#0055a5", fillcolor="#e0e7ef", layer="below")

    # Draw end and side tools at each station
    for idx in range(5):
        x, y = positions[idx]
        sx, sy = side_positions[idx]
        tool_label = labels[idx]
        end_op = ""
        side_op = ""

        if station_data and idx < len(station_data):
            end_op = station_data[idx].get("end_operation", "")
            side_op = station_data[idx].get("side_operation", "")

        # End tool (main station)
        fig.add_trace(go.Scatter(
            x=[x], y=[y], mode="markers+text",
            marker=dict(size=70, color="#f9d900", line=dict(width=3, color="#0055a5")),
            text=[f"<b>{tool_label}</b><br><span style='font-size:18px;color:#444'>{end_op}</span>"] if end_op else [f"<b>{tool_label}</b>"],
            textposition="middle center",
            textfont=dict(size=21),
            hoverinfo="skip",
            showlegend=False
        ))

        # Side tool (offset outward, bigger and square)
        if side_op:
            fig.add_trace(go.Scatter(
                x=[sx], y=[sy], mode="markers+text",
                marker=dict(
                    size=64, color="#7fc97f", line=dict(width=3, color="#0055a5"),
                    symbol="square"
                ),
                text=[f"<b>Side</b><br><span style='font-size:18px;color:#0055a5'>{side_op}</span>"],
                textposition="middle center",
                textfont=dict(size=19, color="#0055a5"),
                hoverinfo="skip",
                showlegend=False
            ))

    # Title (move it a bit lower)
    fig.add_annotation(
        text="<b>Davenport Model B Schematic</b>", xref="paper", yref="paper",
        x=0.5, y=1.12, showarrow=False,
        font=dict(size=24, color="#0055a5", family="Arial Black"),
        align="center"
    )

    # Optional: 2.5D shadow
    fig.add_shape(
        type="circle",
        x0=-0.25, y0=-0.12, x1=0.25, y1=0.08,
        fillcolor="rgba(0,0,0,0.10)", line_color="rgba(0,0,0,0)",
        layer="below"
    )

    fig.update_layout(
        width=800, height=800,
        xaxis=dict(visible=False, range=[-1.8, 1.8], fixedrange=True),
        yaxis=dict(visible=False, range=[-1.8, 1.8], fixedrange=True),
        margin=dict(l=20, r=20, t=160, b=20),  # more top margin
        plot_bgcolor="white",
    )
    st.plotly_chart(fig, use_container_width=True)