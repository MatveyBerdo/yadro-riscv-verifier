#!/usr/bin/env python3
"""
Вспомогательные функции для создания графиков
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional


def create_coverage_chart(history_df: pd.DataFrame, target: float = 92) -> go.Figure:
    """
    Создает график прогресса покрытия
    
    Args:
        history_df: DataFrame с колонками timestamp и coverage
        target: целевое покрытие
    
    Returns:
        Plotly Figure
    """
    fig = px.line(
        history_df,
        x='timestamp',
        y='coverage',
        title="Прогресс верификации",
        labels={'coverage': 'Покрытие (%)', 'timestamp': 'Время'},
        markers=True
    )
    
    fig.add_hline(
        y=target,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Цель {target}%"
    )
    
    fig.update_layout(
        hovermode='x unified',
        height=400
    )
    
    return fig


def create_coverage_heatmap(matrix: np.ndarray, 
                           x_labels: Optional[List] = None,
                           y_labels: Optional[List] = None) -> go.Figure:
    """
    Создает тепловую карту покрытия
    
    Args:
        matrix: 2D массив с покрытием
        x_labels: метки для оси X
        y_labels: метки для оси Y
    
    Returns:
        Plotly Figure
    """
    fig = px.imshow(
        matrix,
        labels=dict(x="Адрес (младшие биты)", y="Адрес (старшие биты)", color="Покрытие"),
        x=x_labels,
        y=y_labels,
        color_continuous_scale='RdYlGn',
        aspect="auto",
        title="Тепловая карта покрытия регистров",
        text_auto='.0f'
    )
    
    fig.update_layout(height=500)
    
    return fig


def create_bug_pie_chart(bugs_df: pd.DataFrame) -> go.Figure:
    """
    Создает круговую диаграмму распределения багов
    
    Args:
        bugs_df: DataFrame с колонкой severity
    
    Returns:
        Plotly Figure
    """
    severity_counts = bugs_df['severity'].value_counts().reset_index()
    severity_counts.columns = ['severity', 'count']
    
    colors = {
        'critical': '#ff4444',
        'high': '#ff8800',
        'medium': '#ffbb33',
        'low': '#00C851'
    }
    
    fig = px.pie(
        severity_counts,
        values='count',
        names='severity',
        title="Распределение багов по серьезности",
        color='severity',
        color_discrete_map=colors,
        hole=0.3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig


def create_file_coverage_bar(files_dict: Dict[str, float]) -> go.Figure:
    """
    Создает столбчатую диаграмму покрытия по файлам
    
    Args:
        files_dict: словарь {имя_файла: покрытие}
    
    Returns:
        Plotly Figure
    """
    df = pd.DataFrame([
        {"file": f, "coverage": c} 
        for f, c in files_dict.items()
    ]).sort_values('coverage')
    
    fig = px.bar(
        df,
        x='coverage',
        y='file',
        orientation='h',
        title="Покрытие по модулям",
        color='coverage',
        color_continuous_scale=['red', 'yellow', 'green'],
        range_color=[0, 100],
        text='coverage'
    )
    
    fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside'
    )
    
    fig.add_vline(
        x=92,
        line_dash="dash",
        line_color="red",
        annotation_text="Цель"
    )
    
    fig.update_layout(height=400)
    
    return fig


def create_gauge_chart(value: float, target: float = 92, 
                       title: str = "Текущее покрытие") -> go.Figure:
    """
    Создает круговой индикатор (gauge chart)
    
    Args:
        value: текущее значение
        target: целевое значение
        title: заголовок
    
    Returns:
        Plotly Figure
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        delta={'reference': target},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 70], 'color': "lightcoral"},
                {'range': [70, 85], 'color': "gold"},
                {'range': [85, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': target
            }
        }
    ))
    
    fig.update_layout(height=300)
    
    return fig


def create_3d_surface(matrix: np.ndarray) -> go.Figure:
    """
    Создает 3D поверхность
    
    Args:
        matrix: 2D массив
    
    Returns:
        Plotly Figure
    """
    fig = go.Figure(data=[
        go.Surface(
            z=matrix,
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Покрытие %")
        )
    ])
    
    fig.update_layout(
        title="3D поверхность покрытия",
        scene=dict(
            xaxis_title="Младшие биты",
            yaxis_title="Старшие биты",
            zaxis_title="Покрытие %"
        ),
        height=600
    )
    
    return fig


def create_animated_coverage(history_df: pd.DataFrame) -> go.Figure:
    """
    Создает анимированный график покрытия
    
    Args:
        history_df: DataFrame с историей
    
    Returns:
        Plotly Figure
    """
    frames = []
    for i in range(1, len(history_df) + 1):
        frame_data = history_df.iloc[:i]
        frames.append(
            go.Frame(
                data=[go.Scatter(
                    x=frame_data['timestamp'],
                    y=frame_data['coverage'],
                    mode='lines+markers'
                )],
                name=f'frame{i}'
            )
        )
    
    fig = go.Figure(
        data=[go.Scatter(
            x=[history_df.iloc[0]['timestamp']],
            y=[history_df.iloc[0]['coverage']],
            mode='lines+markers',
            line=dict(color='blue', width=2)
        )],
        layout=go.Layout(
            title="Анимация прогресса покрытия",
            xaxis=dict(range=[history_df['timestamp'].min(), 
                             history_df['timestamp'].max()], title="Время"),
            yaxis=dict(range=[0, 100], title="Покрытие %"),
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                             method="animate",
                             args=[None])]
            )]
        ),
        frames=frames
    )
    
    return fig