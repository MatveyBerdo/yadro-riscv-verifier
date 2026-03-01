#!/usr/bin/env python3
"""
Страница с отдельными графиками для презентации
Использует реальные данные из JSON файлов
"""

import json
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

# ========== ЗАГРУЗКА ДАННЫХ ==========

@st.cache_data
def load_coverage_data():
    """Загружает данные о покрытии"""
    cov_file = Path("results/latest_coverage.json")
    if cov_file.exists():
        with open(cov_file, 'r') as f:
            return json.load(f)
    return None

@st.cache_data
def load_bugs_data():
    """Загружает данные о багах"""
    bug_file = Path("results/bugs.json")
    if bug_file.exists():
        with open(bug_file, 'r') as f:
            return json.load(f)
    return None

@st.cache_data
def load_test_history():
    """Загружает историю тестов"""
    history_file = Path("results/coverage_history.json")
    if history_file.exists():
        with open(history_file, 'r') as f:
            return json.load(f)
    return None

# Загружаем данные
coverage_data = load_coverage_data()
bugs_data = load_bugs_data()
history_data = load_test_history()

# Преобразуем в DataFrame если есть данные
df_history = None
df_bugs = None
df_test_history = None

if coverage_data and 'history' in coverage_data:
    df_history = pd.DataFrame(coverage_data['history'])
    
if bugs_data:
    df_bugs = pd.DataFrame(bugs_data)
    
if history_data:
    df_test_history = pd.DataFrame(history_data)

# ========== НАСТРОЙКА СТРАНИЦЫ ==========

st.set_page_config(
    page_title="Графики - Yadro Verification",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Галерея графиков")
st.markdown("Отдельные графики для презентации и отчета")

# Если нет данных - показываем предупреждение
if not coverage_data and not bugs_data and not history_data:
    st.warning("⚠️ Нет данных в JSON файлах. Запустите `python scripts/generate_test_data.py` для создания демо-данных.")
else:
    # ========== ЛИНЕЙНЫЕ ГРАФИКИ ==========
    
    st.header("📈 Линейные графики")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if df_history is not None and not df_history.empty:
            # Реальный график из истории
            fig1 = px.line(
                df_history,
                x='timestamp',
                y='coverage',
                title="Реальная динамика покрытия",
                labels={'coverage': 'Покрытие (%)', 'timestamp': 'Время'},
                markers=True
            )
            fig1.add_hline(y=92, line_dash="dash", line_color="red")
        else:
            # Демо-данные если нет реальных
            x = np.linspace(0, 24, 100)
            y = 65 + 20 * np.sin(x/5) + np.random.normal(0, 2, 100)
            y = np.clip(y, 0, 100)
            
            fig1 = px.line(
                x=x, y=y,
                title="Динамика покрытия (демо)",
                labels={'x': 'Время (часы)', 'y': 'Покрытие (%)'}
            )
            fig1.add_hline(y=92, line_dash="dash", line_color="red")
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        if df_test_history is not None and not df_test_history.empty:
            # График из coverage_history.json
            fig2 = px.line(
                df_test_history,
                x='timestamp',
                y='line_rate',
                title="Прогресс покрытия (из истории)",
                labels={'line_rate': 'Покрытие (%)', 'timestamp': 'Время'},
                markers=True
            )
            fig2.add_hline(y=92, line_dash="dash", line_color="red")
        else:
            # Демо-данные
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
            fig2.update_layout(title="Покрытие разных модулей (демо)", xaxis_title="Время")
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # ========== СТОЛБЧАТЫЕ ДИАГРАММЫ ==========
    
    st.header("📊 Столбчатые диаграммы")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if coverage_data and 'files' in coverage_data:
            # Реальные данные по файлам
            files_dict = coverage_data['files']
            df_files = pd.DataFrame([
                {"file": f, "coverage": c} 
                for f, c in files_dict.items()
            ]).sort_values('coverage')
            
            fig3 = px.bar(
                x=df_files['file'], y=df_files['coverage'],
                title="Реальное покрытие по файлам",
                labels={'x': 'Файл', 'y': 'Покрытие (%)'},
                color=df_files['coverage'],
                color_continuous_scale=['red', 'yellow', 'green'],
                text=df_files['coverage']
            )
        else:
            # Демо-данные
            files = ['register_file.py', 'test_gen.py', 'analyzer.py', 'utils.py', 'main.py']
            coverage = np.random.uniform(60, 98, 5)
            
            fig3 = px.bar(
                x=files, y=coverage,
                title="Покрытие по файлам (демо)",
                labels={'x': 'Файл', 'y': 'Покрытие (%)'},
                color=coverage,
                color_continuous_scale=['red', 'yellow', 'green'],
                text=coverage
            )
        
        fig3.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig3.add_hline(y=92, line_dash="dash", line_color="red")
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        if df_bugs is not None and not df_bugs.empty:
            # Реальные данные по статусам багов
            status_counts = df_bugs['status'].value_counts().reset_index()
            status_counts.columns = ['status', 'count']
            
            fig4 = px.bar(
                x=status_counts['status'], y=status_counts['count'],
                title="Реальные баги по статусам",
                labels={'x': 'Статус', 'y': 'Количество'},
                color=status_counts['status'],
                text=status_counts['count']
            )
        else:
            # Демо-данные
            files = ['open', 'fixed', 'verified', 'wontfix']
            counts = np.random.randint(1, 10, 4)
            
            fig4 = px.bar(
                x=files, y=counts,
                title="Баги по статусам (демо)",
                labels={'x': 'Статус', 'y': 'Количество'},
                color=counts,
                text=counts
            )
        
        fig4.update_traces(textposition='outside')
        st.plotly_chart(fig4, use_container_width=True)
    
    # ========== КРУГОВЫЕ ДИАГРАММЫ ==========
    
    st.header("🥧 Круговые диаграммы")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if df_bugs is not None and not df_bugs.empty:
            # Реальные данные по серьезности
            severity_counts = df_bugs['severity'].value_counts().reset_index()
            severity_counts.columns = ['severity', 'count']
            
            fig5 = px.pie(
                severity_counts,
                values='count',
                names='severity',
                title="Реальное распределение багов",
                color='severity',
                color_discrete_map={
                    'critical': '#ff4444',
                    'high': '#ff8800',
                    'medium': '#ffbb33',
                    'low': '#00C851'
                }
            )
        else:
            # Демо-данные
            severities = ['critical', 'high', 'medium', 'low']
            counts = [3, 5, 8, 4]
            
            fig5 = px.pie(
                values=counts, names=severities,
                title="Распределение багов (демо)",
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
        if df_bugs is not None and not df_bugs.empty:
            # Donut chart с реальными данными
            severity_counts = df_bugs['severity'].value_counts().reset_index()
            severity_counts.columns = ['severity', 'count']
            
            fig6 = px.pie(
                severity_counts,
                values='count',
                names='severity',
                title="Donut chart (реальные)",
                color='severity',
                color_discrete_map={
                    'critical': '#ff4444',
                    'high': '#ff8800',
                    'medium': '#ffbb33',
                    'low': '#00C851'
                },
                hole=0.4
            )
        else:
            # Демо-данные
            fig6 = px.pie(
                values=[3,5,8,4], names=['critical','high','medium','low'],
                title="Donut chart (демо)",
                color=['critical','high','medium','low'],
                color_discrete_map={
                    'critical': '#ff4444',
                    'high': '#ff8800',
                    'medium': '#ffbb33',
                    'low': '#00C851'
                },
                hole=0.4
            )
        
        st.plotly_chart(fig6, use_container_width=True)
    
    with col3:
        if df_bugs is not None and not df_bugs.empty:
            # С выноской
            severity_counts = df_bugs['severity'].value_counts().reset_index()
            severity_counts.columns = ['severity', 'count']
            
            fig7 = px.pie(
                severity_counts,
                values='count',
                names='severity',
                title="С выноской (реальные)",
                color='severity',
                color_discrete_map={
                    'critical': '#ff4444',
                    'high': '#ff8800',
                    'medium': '#ffbb33',
                    'low': '#00C851'
                }
            )
        else:
            # Демо-данные
            fig7 = px.pie(
                values=[3,5,8,4], names=['critical','high','medium','low'],
                title="С выноской (демо)",
                color=['critical','high','medium','low'],
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
        # Тепловая карта (пока демо)
        reg_matrix = np.random.uniform(60, 100, (8, 16))
        
        fig8 = px.imshow(
            reg_matrix,
            labels=dict(x="Биты", y="Регистры", color="Покрытие"),
            color_continuous_scale='RdYlGn',
            aspect="auto",
            title="Тепловая карта регистров (демо)",
            text_auto='.0f'
        )
        st.plotly_chart(fig8, use_container_width=True)
    
    with col2:
        # Матрица корреляции (демо)
        corr_matrix = np.random.randn(10, 10)
        corr_matrix = (corr_matrix + corr_matrix.T) / 2
        
        fig9 = px.imshow(
            corr_matrix,
            labels=dict(color="Корреляция"),
            color_continuous_scale='RdBu_r',
            aspect="auto",
            title="Матрица корреляции (демо)",
            text_auto='.2f'
        )
        st.plotly_chart(fig9, use_container_width=True)
    
    # ========== 3D ГРАФИКИ ==========
    
    st.header("🎮 3D визуализация")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 3D поверхность (демо)
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
            title="3D поверхность покрытия (демо)",
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Покрытие %"
            ),
            height=500
        )
        st.plotly_chart(fig10, use_container_width=True)
    
    with col2:
        # 3D scatter (демо)
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
            title="3D scatter plot (демо)",
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
    if df_history is not None and not df_history.empty:
        # Реальные данные
        fig12.add_trace(
            go.Scatter(x=df_history['timestamp'].iloc[:5], y=df_history['coverage'].iloc[:5], 
                      mode='lines+markers', name='coverage'),
            row=1, col=1
        )
    else:
        # Демо
        fig12.add_trace(
            go.Scatter(x=[1,2,3,4], y=[10,15,13,17], mode='lines+markers'),
            row=1, col=1
        )
    
    # Столбчатый
    if coverage_data and 'files' in coverage_data:
        # Реальные данные
        files_list = list(coverage_data['files'].items())[:4]
        fig12.add_trace(
            go.Bar(x=[f[0] for f in files_list], y=[f[1] for f in files_list]),
            row=1, col=2
        )
    else:
        # Демо
        fig12.add_trace(
            go.Bar(x=['A','B','C','D'], y=[20,14,23,19]),
            row=1, col=2
        )
    
    # Круговой
    if df_bugs is not None and not df_bugs.empty:
        # Реальные данные
        sev_counts = df_bugs['severity'].value_counts()
        fig12.add_trace(
            go.Pie(values=sev_counts.values, labels=sev_counts.index),
            row=2, col=1
        )
    else:
        # Демо
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