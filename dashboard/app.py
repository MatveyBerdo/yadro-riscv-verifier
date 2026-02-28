#!/usr/bin/env python3
"""
Главный дашборд для визуализации результатов верификации
Запуск: streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path
import sys
from datetime import datetime, timedelta

# Добавляем путь к проекту
sys.path.append(str(Path(__file__).parent.parent))

# Настройка страницы - ДОЛЖНА БЫТЬ ПЕРВОЙ командой!
st.set_page_config(
    page_title="Yadro RISC-V Verification",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Заголовок
st.title("🔬 Yadro RISC-V Register Verification")
st.markdown("Интерактивный дашборд для мониторинга верификации")


# ========== ЗАГРУЗКА ДАННЫХ ==========

@st.cache_data
def load_coverage_data():
    """Загружает данные о покрытии или создает демо-данные"""
    
    # Пробуем загрузить реальные данные
    cov_file = Path("results/latest_coverage.json")
    if cov_file.exists():
        with open(cov_file, 'r') as f:
            return json.load(f)
    
    # Если нет - создаем демо-данные
    np.random.seed(42)
    
    # Генерируем историю покрытия
    dates = [datetime.now() - timedelta(hours=i) for i in range(24, 0, -1)]
    coverage = 65 + np.cumsum(np.random.normal(0.8, 1, 24))
    coverage = np.clip(coverage, 0, 100)
    
    history = []
    for i, date in enumerate(dates):
        history.append({
            "timestamp": date.isoformat(),
            "coverage": coverage[i]
        })
    
    # Покрытие по файлам
    files = {
        "register_file.py": np.random.uniform(70, 98),
        "test_generator.py": np.random.uniform(65, 95),
        "coverage_analyzer.py": np.random.uniform(80, 99),
        "bug_tracker.py": np.random.uniform(60, 90),
        "api_wrapper.py": np.random.uniform(50, 85),
        "main.py": np.random.uniform(75, 95)
    }
    
    return {
        "history": history,
        "current": history[-1]["coverage"],
        "files": files
    }


@st.cache_data
def load_bugs_data():
    """Загружает данные о багах"""
    
    bug_file = Path("results/bugs.json")
    if bug_file.exists():
        with open(bug_file, 'r') as f:
            return json.load(f)
    
    # Демо-данные
    return [
        {"id": 1, "severity": "critical", "address": "0x24", 
         "description": "Некорректное чтение после записи", 
         "expected": "0x12345678", "actual": "0x87654321",
         "status": "open", "timestamp": "2026-03-07T18:30:00"},
        {"id": 2, "severity": "high", "address": "0x30", 
         "description": "Сброс не обнуляет регистр",
         "expected": "0x00000000", "actual": "0xDEADBEEF",
         "status": "open", "timestamp": "2026-03-07T19:15:00"},
        {"id": 3, "severity": "medium", "address": "0x44", 
         "description": "Задержка при записи > 10ns",
         "expected": "<10ns", "actual": "15ns",
         "status": "verified", "timestamp": "2026-03-07T20:00:00"},
        {"id": 4, "severity": "low", "address": "0x80", 
         "description": "Документация не соответствует поведению",
         "expected": "RW", "actual": "RO",
         "status": "fixed", "timestamp": "2026-03-07T21:30:00"},
        {"id": 5, "severity": "critical", "address": "0x4C", 
         "description": "Запись в защищенный регистр",
         "expected": "0x00000000", "actual": "0xFFFFFFFF",
         "status": "open", "timestamp": "2026-03-07T22:45:00"},
    ]


@st.cache_data
def generate_register_matrix():
    """Генерирует матрицу покрытия регистров 16x16"""
    np.random.seed(42)
    matrix = np.random.uniform(60, 100, (16, 16))
    # Добавляем несколько проблемных зон
    matrix[5, 5] = 45   # низкое покрытие
    matrix[10, 10] = 52  # низкое покрытие
    matrix[3, 12] = 38   # очень низкое
    return matrix


# Загружаем данные
coverage_data = load_coverage_data()
bugs_data = load_bugs_data()
register_matrix = generate_register_matrix()

# Преобразуем в DataFrame для удобства
df_bugs = pd.DataFrame(bugs_data)
df_history = pd.DataFrame(coverage_data.get("history", []))


# ========== БОКОВАЯ ПАНЕЛЬ ==========

with st.sidebar:
    st.header("⚙️ Управление")
    
    # Кнопка обновления
    if st.button("🔄 Обновить данные", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    
    # Фильтры
    st.subheader("🔍 Фильтры")
    
    show_critical = st.checkbox("Критические баги", value=True)
    show_high = st.checkbox("Высокие", value=True)
    show_medium = st.checkbox("Средние", value=False)
    show_low = st.checkbox("Низкие", value=False)
    
    selected_severity = []
    if show_critical: selected_severity.append("critical")
    if show_high: selected_severity.append("high")
    if show_medium: selected_severity.append("medium")
    if show_low: selected_severity.append("low")
    
    st.divider()
    
    # Статус хакатона
    st.subheader("📊 Статус")
    
    # Время до дедлайна
    deadline = datetime(2026, 3, 8, 21, 0)  # 8 марта 21:00
    now = datetime.now()
    time_left = deadline - now
    
    if time_left.total_seconds() > 0:
        hours = int(time_left.total_seconds() // 3600)
        minutes = int((time_left.total_seconds() % 3600) // 60)
        st.metric("⏱ До дедлайна", f"{hours}ч {minutes}м")
    else:
        st.error("🚨 ВРЕМЯ ВЫШЛО!")
    
    # Прогресс-бар
    current_cov = coverage_data.get("current", 0)
    st.progress(min(current_cov / 100, 1.0), 
                text=f"Прогресс: {current_cov:.1f}%")
    
    st.divider()
    
    # Информация о команде
    st.markdown("---")
    st.markdown("🔬 **Команда V-TEAM**")
    st.markdown("Nuclear IT Hack 2026 | Кейс Yadro")


# ========== ОСНОВНЫЕ МЕТРИКИ ==========

col1, col2, col3, col4 = st.columns(4)

with col1:
    current = coverage_data.get("current", 0)
    delta = current - 92
    st.metric(
        "📈 Текущее покрытие",
        f"{current:.1f}%",
        delta=f"{delta:+.1f}%" if delta != 0 else None,
        delta_color="inverse"
    )

with col2:
    st.metric(
        "🎯 Цель",
        "92%",
        help="Целевое покрытие для успешной верификации"
    )

with col3:
    filtered_bugs = df_bugs[df_bugs['severity'].isin(selected_severity)] if selected_severity else df_bugs
    st.metric(
        "🐛 Найдено багов",
        len(filtered_bugs),
        help=f"Всего: {len(df_bugs)}"
    )

with col4:
    critical_count = len(df_bugs[df_bugs['severity'] == 'critical'])
    st.metric(
        "🔴 Критических",
        critical_count,
        help="Требуют немедленного внимания"
    )


# ========== ВКЛАДКИ ==========

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Прогресс покрытия",
    "🔍 Анализ регистров",
    "🐞 Найденные баги",
    "📊 Отчеты"
])


# ========== ВКЛАДКА 1: ПРОГРЕСС ПОКРЫТИЯ ==========

with tab1:
    st.subheader("Динамика покрытия")
    
    if not df_history.empty:
        # Линейный график
        fig_progress = px.line(
            df_history,
            x='timestamp',
            y='coverage',
            title="Прогресс верификации во времени",
            labels={'coverage': 'Покрытие (%)', 'timestamp': 'Время'},
            markers=True
        )
        
        # Добавляем целевую линию
        fig_progress.add_hline(
            y=92,
            line_dash="dash",
            line_color="red",
            annotation_text="Цель 92%",
            annotation_position="top right"
        )
        
        # Добавляем аннотации
        max_cov = df_history['coverage'].max()
        max_idx = df_history['coverage'].idxmax()
        fig_progress.add_annotation(
            x=df_history.loc[max_idx, 'timestamp'],
            y=max_cov,
            text=f"Максимум: {max_cov:.1f}%",
            showarrow=True,
            arrowhead=1
        )
        
        fig_progress.update_layout(
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig_progress, use_container_width=True)
    
    # Покрытие по файлам
    st.subheader("Покрытие по модулям")
    
    files_data = coverage_data.get("files", {})
    if files_data:
        df_files = pd.DataFrame([
            {"file": f, "coverage": c} 
            for f, c in files_data.items()
        ]).sort_values('coverage')
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Горизонтальная бар-чарт
            fig_files = px.bar(
                df_files,
                x='coverage',
                y='file',
                orientation='h',
                title="Покрытие по модулям",
                color='coverage',
                color_continuous_scale=['red', 'yellow', 'green'],
                range_color=[0, 100],
                text='coverage'
            )
            
            fig_files.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside'
            )
            
            fig_files.add_vline(
                x=92,
                line_dash="dash",
                line_color="red",
                annotation_text="Цель"
            )
            
            fig_files.update_layout(height=400)
            st.plotly_chart(fig_files, use_container_width=True)
        
        with col2:
            # Статистика
            st.metric("Среднее", f"{df_files['coverage'].mean():.1f}%")
            st.metric("Медиана", f"{df_files['coverage'].median():.1f}%")
            st.metric("Минимум", f"{df_files['coverage'].min():.1f}%")
            st.metric("Максимум", f"{df_files['coverage'].max():.1f}%")
            
            # Худший файл
            worst = df_files.loc[df_files['coverage'].idxmin()]
            st.warning(f"⚠️ **Требует внимания:** {worst['file']} ({worst['coverage']:.1f}%)")


# ========== ВКЛАДКА 2: АНАЛИЗ РЕГИСТРОВ ==========

with tab2:
    st.subheader("Тепловая карта покрытия регистров")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Тепловая карта 16x16
        fig_heatmap = px.imshow(
            register_matrix,
            labels=dict(
                x="Младшие 4 бита адреса",
                y="Старшие 4 бита адреса",
                color="Покрытие (%)"
            ),
            x=[f"{i:X}" for i in range(16)],
            y=[f"{i:X}" for i in range(16)],
            color_continuous_scale='RdYlGn',
            aspect="auto",
            title="Покрытие по адресному пространству",
            text_auto='.0f'
        )
        
        fig_heatmap.update_layout(height=600)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Легенда")
        st.markdown("🟢 **90-100%** - Отлично")
        st.markdown("🟡 **80-89%** - Хорошо")
        st.markdown("🟠 **70-79%** - Требует внимания")
        st.markdown("🔴 **<70%** - Критично")
        
        st.divider()
        
        # Поиск проблемных адресов
        st.markdown("### 🔍 Проблемные адреса")
        
        threshold = st.slider(
            "Показать адреса с покрытием ниже",
            min_value=0,
            max_value=100,
            value=80,
            step=5
        )
        
        # Находим адреса ниже порога
        problem_addrs = []
        for i in range(16):
            for j in range(16):
                if register_matrix[i, j] < threshold:
                    addr = f"0x{i:X}{j:X}"
                    problem_addrs.append({
                        "address": addr,
                        "coverage": f"{register_matrix[i, j]:.1f}%"
                    })
        
        if problem_addrs:
            df_problems = pd.DataFrame(problem_addrs)
            st.dataframe(df_problems, use_container_width=True, hide_index=True)
        else:
            st.success(f"Нет адресов с покрытием ниже {threshold}%")
    
    # 3D визуализация (опционально)
    with st.expander("🎮 3D-визуализация покрытия"):
        fig_3d = go.Figure(data=[
            go.Surface(
                z=register_matrix,
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Покрытие %")
            )
        ])
        
        fig_3d.update_layout(
            title="3D-поверхность покрытия регистров",
            scene=dict(
                xaxis_title="Младшие биты",
                yaxis_title="Старшие биты",
                zaxis_title="Покрытие %"
            ),
            height=600
        )
        
        st.plotly_chart(fig_3d, use_container_width=True)


# ========== ВКЛАДКА 3: НАЙДЕННЫЕ БАГИ ==========

with tab3:
    st.subheader("Анализ найденных дефектов")
    
    if not df_bugs.empty:
        # Фильтруем по выбранной серьезности
        if selected_severity:
            df_filtered = df_bugs[df_bugs['severity'].isin(selected_severity)]
        else:
            df_filtered = df_bugs
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Круговая диаграмма по серьезности
            severity_counts = df_bugs['severity'].value_counts().reset_index()
            severity_counts.columns = ['severity', 'count']
            
            fig_pie = px.pie(
                severity_counts,
                values='count',
                names='severity',
                title="Распределение багов по серьезности",
                color='severity',
                color_discrete_map={
                    'critical': '#ff4444',
                    'high': '#ff8800',
                    'medium': '#ffbb33',
                    'low': '#00C851'
                },
                hole=0.3
            )
            
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Статус багов
            status_counts = df_bugs['status'].value_counts().reset_index()
            status_counts.columns = ['status', 'count']
            
            fig_status = px.bar(
                status_counts,
                x='status',
                y='count',
                title="Баги по статусам",
                color='status',
                color_discrete_map={
                    'open': '#ff4444',
                    'verified': '#ffbb33',
                    'fixed': '#00C851',
                    'wontfix': '#aaaaaa'
                },
                text='count'
            )
            
            fig_status.update_traces(textposition='outside')
            st.plotly_chart(fig_status, use_container_width=True)
        
        # Таблица багов
        st.subheader("Детальный список багов")
        
        # Настраиваем отображение
        column_config = {
            "id": st.column_config.NumberColumn("ID", width="small"),
            "severity": st.column_config.SelectboxColumn(
                "Серьезность",
                options=['critical', 'high', 'medium', 'low'],
                width="small"
            ),
            "address": st.column_config.TextColumn("Адрес", width="small"),
            "description": st.column_config.TextColumn("Описание", width="large"),
            "status": st.column_config.SelectboxColumn(
                "Статус",
                options=['open', 'fixed', 'verified', 'wontfix'],
                width="small"
            ),
            "timestamp": st.column_config.DatetimeColumn("Обнаружен", width="medium")
        }
        
        # Применяем цветовое кодирование
        def color_severity(val):
            colors = {
                'critical': 'background-color: #ff4444; color: white',
                'high': 'background-color: #ff8800; color: white',
                'medium': 'background-color: #ffbb33; color: black',
                'low': 'background-color: #00C851; color: white'
            }
            return colors.get(val, '')
        
        st.dataframe(
            df_filtered,
            column_config=column_config,
            use_container_width=True,
            hide_index=True
        )
        
        # Статистика
        st.divider()
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Открыто", len(df_bugs[df_bugs['status'] == 'open']))
        with col2:
            st.metric("Исправлено", len(df_bugs[df_bugs['status'] == 'fixed']))
        with col3:
            st.metric("Верифицировано", len(df_bugs[df_bugs['status'] == 'verified']))
        with col4:
            st.metric("Не будет исправлено", len(df_bugs[df_bugs['status'] == 'wontfix']))
    
    else:
        st.info("Нет данных о багах. Добавьте баги через bug_tracker.py")


# ========== ВКЛАДКА 4: ОТЧЕТЫ ==========

with tab4:
    st.subheader("Генерация отчетов")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Текстовый отчет")
        if st.button("Сгенерировать отчет в Markdown", use_container_width=True):
            # Создаем отчет
            report = []
            report.append("# Отчет о верификации RISC-V регистрового блока\n")
            report.append(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            report.append("## Сводка\n")
            report.append(f"- Покрытие: {coverage_data.get('current', 0):.1f}%")
            report.append(f"- Всего багов: {len(df_bugs)}")
            report.append(f"- Критических: {len(df_bugs[df_bugs['severity'] == 'critical'])}")
            
            report_text = "\n".join(report)
            
            # Показываем в дашборде
            st.markdown("**Предпросмотр:**")
            st.markdown(report_text)
            
            # Сохраняем в файл
            report_file = f"results/report_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
            Path("results").mkdir(exist_ok=True)
            with open(report_file, 'w') as f:
                f.write(report_text)
            
            st.success(f"✅ Отчет сохранен: {report_file}")
    
    with col2:
        st.markdown("### 📊 Экспорт данных")
        
        export_format = st.selectbox(
            "Формат экспорта",
            ["JSON", "CSV", "HTML"]
        )
        
        if st.button("Экспортировать", use_container_width=True):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            
            if export_format == "JSON":
                # Экспорт в JSON
                export_data = {
                    "coverage": coverage_data,
                    "bugs": bugs_data,
                    "timestamp": datetime.now().isoformat()
                }
                
                filename = f"results/export_{timestamp}.json"
                with open(filename, 'w') as f:
                    json.dump(export_data, f, indent=2)
                st.success(f"✅ Экспортировано в {filename}")
            
            elif export_format == "CSV":
                # Экспорт багов в CSV
                filename = f"results/bugs_{timestamp}.csv"
                df_bugs.to_csv(filename, index=False)
                st.success(f"✅ Экспортировано в {filename}")
            
            else:
                # Экспорт в HTML (весь дашборд)
                st.info("HTML-экспорт будет доступен позже")
    
    # Графики для отчета
    st.divider()
    st.subheader("📈 Графики для отчета")
    
    if st.button("Сгенерировать все графики"):
        # Создаем папку для отчетов
        report_dir = Path("results/report_images")
        report_dir.mkdir(exist_ok=True)
        
        # График прогресса
        if not df_history.empty:
            fig_progress.write_html(report_dir / "progress.html")
        
        # Тепловая карта
        fig_heatmap.write_html(report_dir / "heatmap.html")
        
        # Круговая диаграмма
        if 'fig_pie' in locals():
            fig_pie.write_html(report_dir / "bugs_pie.html")
        
        st.success(f"✅ Графики сохранены в {report_dir}/")


# ========== FOOTER ==========

st.divider()
st.markdown(
    "<div style='text-align: center; color: gray; padding: 20px;'>"
    "🔬 **Команда V-TEAM** | Nuclear IT Hack 2026 | Кейс Yadro<br>"
    "📊 Дашборд построен на Streamlit + Plotly"
    "</div>",
    unsafe_allow_html=True
)