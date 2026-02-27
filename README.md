# Yadro RISC-V Register Verifier

## Nuclear IT Hack 2026 | Кейс Yadro

---

## О проекте

Репозиторий команды **[Название команды]** для участия в хакатоне Nuclear IT Hack 2026.

**Кейс:** Верификация RISC-V регистрового блока от Yadro  
**Задача:** За 24 часа разработать тесты на Python, достичь >92% покрытия и найти реальные баги в "черном ящике"  
**API:** `reg_access(addr, data, rw)`

---

## Команда

| Участник | Роль | Контакт |
|----------|------|---------|
| | Team Lead | @ |
| | Разработка тестов | @ |
| | Анализ покрытия | @ |
| | Скриптинг и автоматизация | @ |

---

## Технологии

- Python 3.8+
- pytest / pytest-cov
- Git / GitHub
- RISC-V / SystemRDL

---

## Быстрый старт

```bash
# Клонируем репозиторий
git clone https://github.com/your-team/yadro-riscv-verifier.git
cd yadro-riscv-verifier

# Создаем виртуальное окружение
python3 -m venv venv

# Активируем
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Устанавливаем зависимости
pip install -r requirements.txt

# Запускаем тесты
pytest tests/ --cov=src
