import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

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
                "Log Compute: %{y:.2f}<br>" +
                "<extra></extra>"
            )
        ))

# Update layout
fig.update_layout(
    title=dict(
        text='Language Model Training Compute Trends',
        font=dict(size=24),
        y=0.95
    ),
    xaxis=dict(
        title='Year',
        titlefont=dict(size=16),
        gridcolor='lightgray',
        gridwidth=0.5,
        showgrid=True
    ),
    yaxis=dict(
        title='Training Compute (log10 FLOP)',
        titlefont=dict(size=16),
        gridcolor='lightgray',
        gridwidth=0.5,
        showgrid=True
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
        font=dict(size=14)
    ),
    margin=dict(r=150)  # 为图例留出空间
)

# Save plots
fig.write_html("compute_trend.html")  # 交互式HTML
fig.write_image("compute_trend.pdf")  # 静态PDF
fig.write_image("compute_trend.png")  # 静态PNG

print("\nPlots have been saved as 'compute_trend.html', 'compute_trend.pdf', and 'compute_trend.png'") 