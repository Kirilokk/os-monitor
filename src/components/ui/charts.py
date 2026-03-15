import plotly.graph_objects as go


def build_vram_chart(vram_used, vram_total, vram_percent):
    fig = go.Figure(
        go.Pie(
            values=[vram_used, vram_total - vram_used],
            labels=["Used", "Free"],
            hole=0.65,
            textinfo="none",
        )
    )

    fig.update_layout(
        height=250,
        margin=dict(t=0, b=0, l=0, r=0),
        annotations=[dict(text=f"{vram_percent:.0f}%", showarrow=False, font_size=28)],
    )

    return fig
