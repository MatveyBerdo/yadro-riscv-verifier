# Yadro RISC-V Register Verifier

<div align="center">

## ⚡ Nuclear IT Hack 2026 | Кейс Yadro ⚡

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![pytest](https://img.shields.io/badge/pytest-7.4.0-green.svg)](https://pytest.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25.0-red.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.14.1-blue.svg)](https://plotly.com/)

</div>

---

## 📋 О проекте

**Кейс Yadro**: Верификация RISC-V регистрового блока с использованием SystemRDL и coverage-driven подхода.

**Технологический стек:**
- **SystemRDL** — описание регистровой модели
- **pytest** + **coverage-driven** — разработка тестов с фокусом на покрытие
- **Streamlit** + **Plotly** — визуализация результатов верификации
- **RTL-верификация** — проверка Register Transfer Level описания

**Цель**: Достичь >92% покрытия и найти реальные баги в "черном ящике" Yadro.

---

## 👥 Команда UNITY

| Участник | Роль | Контакт |
|----------|------|---------|
| | Team Lead, SystemRDL | @ |
| | Разработка тестов, coverage | @ |
| | Streamlit/Plotly визуализация | @ |
| | Автоматизация, скриптинг | @ |

---

## 🚀 Быстрый старт

```bash
# Клонирование
git clone https://github.com/your-team/yadro-riscv-verifier.git
cd yadro-riscv-verifier

# Виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Установка зависимостей
pip install -r requirements.txt

# Запуск тестов
pytest tests/ --cov=src

# Запуск дашборда
streamlit run scripts/dashboard.py
