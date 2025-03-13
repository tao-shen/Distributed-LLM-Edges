import plotly.graph_objects as go
import pandas as pd
import numpy as np
import base64
from pathlib import Path


# 定义设备位置
devices = pd.DataFrame(
    [
        # 北美洲 (北美东西海岸)
        {
            "type": "smartphone",
            "lat": 60,
            "lon": -120,
            "name": "West Coast Mobile",
            "size": 35,
            "emoji": "📱",
        },
        {
            "type": "laptop",
            "lat": 40,
            "lon": -100,
            "name": "East Coast Laptop",
            "size": 35,
            "emoji": "💻",
        },
        # 南美洲 (南美洲南北部)
        {
            "type": "tv",
            "lat": -0,
            "lon": -70,
            "name": "South America TV",
            "size": 35,
            "emoji": "🎮",
        },
        {
            "type": "robot",
            "lat": -20,
            "lon": -60,
            "name": "South America Robot",
            "size": 30,
            "emoji": "🤖",
        },
        # 欧洲 (西欧和东欧)
        {
            "type": "watch",
            "lat": 50,
            "lon": 20,
            "name": "East Europe Watch",
            "size": 25,
            "emoji": "⌚",
        },
        # 亚洲 (东亚和东南亚)
        {
            "type": "desktop",
            "lat": 60,
            "lon": 90,
            "name": "West Europe Desktop",
            "size": 35,
            "emoji": "🖥️",
        },
        {
            "type": "tablet",
            "lat": 40,
            "lon": 60,
            "name": "East Asia Tablet",
            "size": 30,
            "emoji": "📱",
        },
        {
            "type": "iot",
            "lat": 30,
            "lon": 90,
            "name": "Southeast Asia IoT",
            "size": 30,
            "emoji": "🚗",
        },
        {
            "type": "robot",
            "lat": 35,
            "lon": 140,
            "name": "South America Robot",
            "size": 30,
            "emoji": "🤖",
        },
        # 大洋洲 (澳大利亚东西部)
        {
            "type": "speaker",
            "lat": -25,
            "lon": 130,
            "name": "East Australia Speaker",
            "size": 30,
            "emoji": "🔊",
        },
        # {'type': 'car', 'lat': -30, 'lon': 120, 'name': 'West Australia Car', 'size': 35, 'emoji': '🚗'},
        # 非洲 (北非和南非)
        {
            "type": "smartphone",
            "lat": 18,
            "lon": 0,
            "name": "North Africa Mobile",
            "size": 35,
            "emoji": "📱",
        },
        {
            "type": "tv",
            "lat": -10,
            "lon": 25,
            "name": "South Africa TV",
            "size": 35,
            "emoji": "📺",
        },
    ]
)

# 创建云的位置（调整位置使LLM更高）
cloud_points = pd.DataFrame(
    [
        {
            "lat": 80,
            "lon": 15,
            "size": 80,
            "name": "LLM Cloud",
            "emoji": "☁️",
        },  # 更高的位置，更大的尺寸
    ]
)

# 创建空白地图
fig = go.Figure()

# 添加LLM云标记
fig.add_trace(
    go.Scattergeo(
        lon=[cloud_points.iloc[0]["lon"]],
        lat=[cloud_points.iloc[0]["lat"] - 10],
        mode="text",
        text=["☁️"],
        textposition="middle center",
        textfont=dict(
            size=140,  # 更大的云朵尺寸
        ),
        hovertemplate="<b>Large Language Model</b><br>"
        + "Global AI Processing Hub<br>"
        + "<extra></extra>",
        showlegend=False,
    )
)

# 添加设备图标和它们的SLM云
for _, device in devices.iterrows():
    # 添加设备图标
    fig.add_trace(
        go.Scattergeo(
            lon=[device["lon"]],
            lat=[device["lat"]],
            text=[device["emoji"]],
            mode="text",
            textposition="middle center",
            textfont=dict(
                size=60,  # 更大的设备图标
            ),
            hovertext=[device["name"]],
            hovertemplate="<b>%{hovertext}</b><extra></extra>",
            showlegend=False,
        )
    )

    # 添加设备的云标记
    fig.add_trace(
        go.Scattergeo(
            lon=[device["lon"] + 11],  # 更靠右
            lat=[device["lat"] + 2.5],  # 更靠上
            mode="text",
            text=["☁️"],
            textposition="middle center",
            textfont=dict(
                size=55,  # 更大的SLM云朵
            ),
            hovertemplate="<b>Small Language Model</b><br>"
            + "Device Processing Node<br>"
            + "<extra></extra>",
            showlegend=False,
        )
    )

    # 添加设备的SLM到主LLM的连接线
    fig.add_trace(
        go.Scattergeo(
            lon=[device["lon"] + 10, cloud_points.iloc[0]["lon"]],  # 调整起点
            lat=[device["lat"] + 2.5, cloud_points.iloc[0]["lat"] - 10],
            mode="lines",
            line=dict(color="#666666", width=1.5, dash="dash"),  # 加粗连接线
            hoverinfo="skip",
            showlegend=False,
        )
    )

# 更新布局
fig.update_layout(
    # 地图样式
    geo=dict(
        showframe=False,  # 隐藏边框
        showcoastlines=True,  # 显示海岸线
        coastlinecolor="rgba(165, 214, 231, 0.7)",  # 半透明的柔和蓝色海岸线
        showland=True,  # 显示陆地
        landcolor="rgba(232, 244, 234, 0.6)",  # 半透明的柔和薄荷绿陆地
        showocean=True,  # 显示海洋
        oceancolor="rgba(219, 243, 250, 0.4)",  # 更透明的淡蓝色海洋
        showlakes=True,  # 显示湖泊
        lakecolor="rgba(219, 243, 250, 0.5)",  # 半透明的淡蓝色湖泊
        showcountries=True,  # 显示国界
        countrycolor="rgba(255, 255, 255, 0.8)",  # 半透明的白色国界
        countrywidth=0.3,  # 更细的国界线宽度，增加精致感
        showsubunits=False,  # 不显示次级行政区
        projection_type="equirectangular",
        center=dict(lon=15, lat=15),
        scope="world",
        lonaxis=dict(range=[-150, 150]),
        lataxis=dict(range=[-50, 90]),
    ),
    # 图表尺寸 - 设置宽高比
    margin=dict(r=0, t=0, l=0, b=0, pad=0),
    width=1600,
    height=800,  # 恢复原来的高度
    # 移除标题
    showlegend=False,
    # 启用自动缩放
    autosize=False,
)

# 更新配置
config = {
    "displayModeBar": False,
    "responsive": True,  # 启用响应式布局
    "scrollZoom": False,
    "staticPlot": False,
}

fig.write_html("static/htmls/bg.html", config=config)  # 保存交互式HTML，应用配置
# fig.write_image("icml25_position/figs/fedllm.pdf")  # 保存静态PDF
# fig.write_image("icml25_position/figs/fedllm.svg")  # 保存静态SVG
fig.show(config=config)  # 显示图表，应用配置
