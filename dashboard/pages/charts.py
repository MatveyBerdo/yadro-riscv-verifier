#!/usr/bin/env python3
"""
Страница с отдельными графиками для презентации
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="Графики - Yadro Verification",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Галерея графиков")
st.markdown("Отдельные графики для презентации и отчета")

# Генерируем демо-данные
np.random.seed(42)

# ========== ЛИНЕЙНЫЕ ГРАФИКИ ==========

st.header("📈 Линейные графики")

col1, col2 = st.columns(2)

with col1:
    # Простой линейный
    x = np.linspace(0, 24, 100)
    y = 65 + 20 * np.sin(x/5) + np.random.normal(0, 2, 100)
    y = np.clip(y, 0, 100)
    
    fig1 = px.line(
        x=x, y=y,
        title="Динамика покрытия с шумом",
        labels={'x': 'Время (часы)', 'y': 'Покрытие (%)'}
    )
    fig1.add_hline(y=92, line_dash="dash", line_color="red")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Множественные линии
    df_multi = pd.DataFrame({
        'time': np.linspace(0, 24, 50),
        'register_file': 70 + 20 * np.sin(np.linspace(0, 4, 50)) + np.random.normal(0, 1, 50),
        'test_gen': 65 + 15 * np.cos(np.linspace(0, 3, 50)) + np.random.normal(0, 1, 50),
        'analyzer': 80 + 10 * np.sin(np.linspace(0, 2, 50)) + np.random.normal(0, 0.5, 50)
    })
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_multi['time'], y=df_multi['register_file'], 
                              mode='lines+markers', name='register_file'))
    fig2.add_trace(go.Scatter(x=df_multi['time'], y=df_multi['test_gen'], 
                              mode='lines+markers', name='test_gen'))
    fig2.add_trace(go.Scatter(x=df_multi['time'], y=df_multi['analyzer'], 
                              mode='lines+markers', name='analyzer'))
    fig2.add_hline(y=92, line_dash="dash", line_color="red")
    fig2.update_layout(title="Покрытие разных модулей", xaxis_title="Время")
    st.plotly_chart(fig2, use_container_width=True)


# ========== СТОЛБЧАТЫЕ ДИАГРАММЫ ==========

st.header("📊 Столбчатые диаграммы")

col1, col2 = st.columns(2)

with col1:
    # Вертикальные столбцы
    files = ['register_file.py', 'test_gen.py', 'analyzer.py', 'utils.py', 'main.py']
    coverage = np.random.uniform(60, 98, 5)
    
    fig3 = px.bar(
        x=files, y=coverage,
        title="Покрытие по файлам",
        labels={'x': 'Файл', 'y': 'Покрытие (%)'},
        color=coverage,
        color_continuous_scale=['red', 'yellow', 'green'],
        text=coverage
    )
    fig3.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig3.add_hline(y=92, line_dash="dash", line_color="red")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Горизонтальные столбцы
    fig4 = px.bar(
        y=files, x=coverage,
        orientation='h',
        title="Покрытие по файлам (горизонтально)",
        labels={'x': 'Покрытие (%)', 'y': 'Файл'},
        color=coverage,
        color_continuous_scale=['red', 'yellow', 'green'],
        text=coverage
    )
    fig4.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig4.add_vline(x=92, line_dash="dash", line_color="red")
    st.plotly_chart(fig4, use_container_width=True)


# ========== КРУГОВЫЕ ДИАГРАММЫ ==========

st.header("🥧 Круговые диаграммы")

col1, col2, col3 = st.columns(3)

with col1:
    # Простая круговая
    severities = ['critical', 'high', 'medium', 'low']
    counts = [3, 5, 8, 4]
    
    fig5 = px.pie(
        values=counts, names=severities,
        title="Распределение багов",
        color=severities,
        color_discrete_map={
            'critical': '#ff4444',
            'high': '#ff8800',
            'medium': '#ffbb33',
            'low': '#00C851'
        }
    )
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    # С отверстием (donut)
    fig6 = px.pie(
        values=counts, names=severities,
        title="Donut chart",
        hole=0.4,
        color=severities,
        color_discrete_map={
            'critical': '#ff4444',
            'high': '#ff8800',
            'medium': '#ffbb33',
            'low': '#00C851'
        }
    )
    st.plotly_chart(fig6, use_container_width=True)

with col3:
    # С выноской
    fig7 = px.pie(
        values=counts, names=severities,
        title="С выноской",
        color=severities,
        color_discrete_map={
            'critical': '#ff4444',
            'high': '#ff8800',
            'medium': '#ffbb33',
            'low': '#00C851'
        }
    )
    fig7.update_traces(textposition='outside', textinfo='percent+label')
    st.plotly_chart(fig7, use_container_width=True)


# ========== ТЕПЛОВЫЕ КАРТЫ ==========

st.header("🔥 Тепловые карты")

col1, col2 = st.columns(2)

with col1:
    # Тепловая карта регистров
    reg_matrix = np.random.uniform(60, 100, (8, 16))
    
    fig8 = px.imshow(
        reg_matrix,
        labels=dict(x="Биты", y="Регистры", color="Покрытие"),
        color_continuous_scale='RdYlGn',
        aspect="auto",
        title="Тепловая карта регистров",
        text_auto='.0f'
    )
    st.plotly_chart(fig8, use_container_width=True)

with col2:
    # Correlation matrix
    corr_matrix = np.random.randn(10, 10)
    corr_matrix = (corr_matrix + corr_matrix.T) / 2  # симметричная
    
    fig9 = px.imshow(
        corr_matrix,
        labels=dict(color="Корреляция"),
        color_continuous_scale='RdBu_r',
        aspect="auto",
        title="Матрица корреляции",
        text_auto='.2f'
    )
    st.plotly_chart(fig9, use_container_width=True)


# ========== 3D ГРАФИКИ ==========

st.header("🎮 3D визуализация")

col1, col2 = st.columns(2)

with col1:
    # 3D поверхность
    X, Y = np.meshgrid(range(10), range(10))
    Z = np.random.uniform(60, 100, (10, 10))
    
    fig10 = go.Figure(data=[
        go.Surface(
            z=Z,
            colorscale='RdYlGn',
            showscale=True
        )
    ])
    
    fig10.update_layout(
        title="3D поверхность покрытия",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Покрытие %"
        ),
        height=500
    )
    st.plotly_chart(fig10, use_container_width=True)

with col2:
    # 3D scatter
    n_points = 50
    x = np.random.randn(n_points) * 10
    y = np.random.randn(n_points) * 10
    z = np.random.randn(n_points) * 10
    colors = np.random.randn(n_points)
    
    fig11 = go.Figure(data=[
        go.Scatter3d(
            x=x, y=y, z=z,
            mode='markers',
            marker=dict(
                size=8,
                color=colors,
                colorscale='Viridis',
                showscale=True
            )
        )
    ])
    
    fig11.update_layout(
        title="3D scatter plot",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z"
        ),
        height=500
    )
    st.plotly_chart(fig11, use_container_width=True)


# ========== КОМБИНИРОВАННЫЕ ГРАФИКИ ==========

st.header("🔄 Комбинированные графики")

# Subplot с разными типами
fig12 = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Линейный", "Столбчатый", "Круговой", "Точечный"),
    specs=[
        [{"type": "scatter"}, {"type": "bar"}],
        [{"type": "pie"}, {"type": "scatter"}]
    ]
)

# Линейный
fig12.add_trace(
    go.Scatter(x=[1,2,3,4], y=[10,15,13,17], mode='lines+markers'),
    row=1, col=1
)

# Столбчатый
fig12.add_trace(
    go.Bar(x=['A','B','C','D'], y=[20,14,23,19]),
    row=1, col=2
)

# Круговой
fig12.add_trace(
    go.Pie(values=[30,20,25,25], labels=['A','B','C','D']),
    row=2, col=1
)

# Точечный
fig12.add_trace(
    go.Scatter(x=np.random.randn(20), y=np.random.randn(20), mode='markers'),
    row=2, col=2
)

fig12.update_layout(height=600, showlegend=False, title_text="Комбинированный дашборд")
st.plotly_chart(fig12, use_container_width=True)