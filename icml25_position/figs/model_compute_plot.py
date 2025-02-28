import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from scipy import stats

# Read the CSV file
df = pd.read_csv('notable_ai_models.csv')

# Filter for Language models only
df = df[df['Domain'].str.contains('Language', na=False)]

# Filter for specified companies and their important models
selected_companies = {
    'OpenAI': ['GPT-4', 'GPT-3.5', 'GPT-3'],
    'Google': ['PaLM', 'PaLM-2', 'Gemini'],
    'Anthropic': ['Claude', 'Claude 2', 'Claude 3'],
    'Meta': ['LLaMA', 'LLaMA-2', 'LLaMA-3'],
    'DeepSeek': ['DeepSeek-MoE', 'DeepSeek-67B'],
    'Alibaba': ['Qwen-72B', 'Qwen-2', 'Qwen-1.5']
}

# Create color scheme
company_colors = {
    'OpenAI': '#FF4B4B',      # 红色
    'Google': '#4285F4',      # Google蓝
    'Anthropic': '#674EA7',   # 紫色
    'Meta': '#0668E1',        # Meta蓝
    'DeepSeek': '#00A36C',    # 绿色
    'Alibaba': '#FF6A00'      # 橙色
}

# Filter for major models
df['is_major'] = False
for company, models in selected_companies.items():
    for model in models:
        df.loc[df['Model'].str.contains(model, case=False, na=False) & 
               (df['Organization'] == company), 'is_major'] = True

df = df[df['is_major']]

# Convert and clean data
df['Year'] = pd.to_datetime(df['Publication date'], errors='coerce').dt.year
df['Training compute (FLOP)'] = pd.to_numeric(df['Training compute (FLOP)'], errors='coerce')
df['Log Compute'] = np.log10(df['Training compute (FLOP)'].replace(0, np.nan))
df['Training dataset size (datapoints)'] = pd.to_numeric(df['Training dataset size (datapoints)'], errors='coerce')
df['Log Dataset Size'] = np.log10(df['Training dataset size (datapoints)'].replace(0, np.nan))

# Remove rows with missing values
df = df.dropna(subset=['Year', 'Log Compute'])

# Calculate axis ranges with padding
year_min = df['Year'].min()
year_max = df['Year'].max()
year_range = year_max - year_min
year_padding = year_range * 0.05  # 5% padding

compute_min = df['Log Compute'].min()
compute_max = df['Log Compute'].max()
compute_range = compute_max - compute_min
compute_padding = compute_range * 0.1  # 10% padding

# Set marker sizes
default_size = 20
df['Marker Size'] = default_size
valid_sizes = df['Log Dataset Size'].notna()
if valid_sizes.any():
    min_size = df.loc[valid_sizes, 'Log Dataset Size'].min()
    max_size = df.loc[valid_sizes, 'Log Dataset Size'].max()
    df.loc[valid_sizes, 'Marker Size'] = ((df.loc[valid_sizes, 'Log Dataset Size'] - min_size) / (max_size - min_size)) * 50 + 20

# Create figure
fig = go.Figure()

# Calculate trend line
x = df['Year'].values
y = df['Log Compute'].values
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
line_x = np.array([year_min - year_padding, year_max + year_padding])
line_y = slope * line_x + intercept

# Add trend line
fig.add_trace(go.Scatter(
    x=line_x,
    y=line_y,
    mode='lines',
    name='Trend (2x/year)',
    line=dict(color='rgba(0,0,0,0.3)', dash='dash'),
    hovertemplate="Year: %{x}<br>Log Compute: %{y:.2f}<extra></extra>"
))

# Add traces for each company
for company, color in company_colors.items():
    mask = df['Organization'] == company
    if mask.any():
        company_data = df[mask]
        
        # Add scatter plot
        fig.add_trace(go.Scatter(
            x=company_data['Year'],
            y=company_data['Log Compute'],
            mode='markers+text',
            name=company,
            marker=dict(
                size=company_data['Marker Size'],
                color=color,
                opacity=0.8,
                line=dict(width=1, color='white')
            ),
            text=company_data['Model'],
            textposition="top center",
            hovertemplate=(
                "<b>%{text}</b><br>" +
                "Year: %{x}<br>" +
                "Training Compute: 10^%{y:.1f} FLOP<br>" +
                "<extra></extra>"
            )
        ))

# Add deep learning era highlight
fig.add_vrect(
    x0=2012,
    x1=year_max + year_padding,
    fillcolor="rgba(200,200,255,0.2)",
    layer="below",
    line_width=0,
    annotation_text="Deep Learning Era",
    annotation_position="top right",
)

# Update layout
fig.update_layout(
    title=dict(
        text='Training Compute (FLOP)',
        font=dict(size=24),
        y=0.95
    ),
    xaxis=dict(
        title='Publication date',
        titlefont=dict(size=16),
        gridcolor='rgba(200,200,200,0.2)',
        gridwidth=1,
        showgrid=True,
        range=[year_min - year_padding, year_max + year_padding],
        dtick=1  # 每年一个刻度
    ),
    yaxis=dict(
        title='Training compute (FLOP)',
        titlefont=dict(size=16),
        gridcolor='rgba(200,200,200,0.2)',
        gridwidth=1,
        showgrid=True,
        range=[compute_min - compute_padding, compute_max + compute_padding],
        dtick=2
    ),
    plot_bgcolor='white',
    width=1200,
    height=800,
    showlegend=True,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=1.02,
        font=dict(size=14),
        bgcolor='rgba(255,255,255,0.8)'
    ),
    margin=dict(r=150),  # 为图例留出空间
    annotations=[
        dict(
            x=(year_min + year_max) / 2,
            y=compute_min + compute_range * 0.3,
            text="~2x/year",
            showarrow=False,
            font=dict(size=14),
            textangle=-30
        )
    ]
)

# Save plots
fig.write_html("compute_trend.html")  # 交互式HTML
fig.write_image("compute_trend.pdf")  # 静态PDF
fig.write_image("compute_trend.png")  # 静态PNG

print("\nPlots have been saved as 'compute_trend.html', 'compute_trend.pdf', and 'compute_trend.png'")