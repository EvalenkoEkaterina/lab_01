# Toolkit — калькулятор и конвертер

Лабораторная работа №1 по предмету "Программирование на Python"

## Что делает программа

- **Калькулятор** — вычисляет математические выражения с операциями `+`, `-`, `*`, `/`
- **Конвертер** — переводит единицы измерения (длина, масса, температура)

## Установка

```bash
# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установить пакет в editable-режиме
pip install -e .
```

После установки команда `python -m toolkit` работает из любой папки — не только из `src`.

## Использование

### Калькулятор

```bash
python -m toolkit calc "2+3*4"
# 14

python -m toolkit calc "10 / 4"
# 2.5

python -m toolkit calc "-2 * -3"
# 6

python -m toolkit calc "1+-2"
# -1
```

Поддерживает:

- Целые и вещественные числа
- Операции: `+`, `-`, `*`, `/`
- Унарные `+` и `-`
- Пробелы между токенами игнорируются
- Приоритет `*` и `/` над `+` и `-`

### Конвертер

```bash
python -m toolkit convert 1000 --from mm --to m
# 1

python -m toolkit convert 1.5 --from km --to m
# 1500

python -m toolkit convert 0 --from c --to f
# 32

python -m toolkit convert -273.15 --from c --to k
# 0
```

Поддерживает:

- Длина: `mm`, `cm`, `m`, `km`
- Масса: `g`, `kg`
- Температура: `c`, `f`, `k`
- Регистр не важен (`MM` = `mm`)
- Конвертация между разными группами запрещена
- Температура ниже абсолютного нуля запрещена

### Справка

```bash
python -m toolkit --help
```

## Ошибки

CLI выводит ошибку в `stderr` и завершается с кодом `2`. Успешная команда завершается с кодом `0`.

Обрабатываются:

- пустое выражение (`EmptyExpressionError`)
- недопустимый символ (`InvalidCharacterError`)
- пропущенный операнд (`ExpressionError`)
- два бинарных оператора подряд (`ExpressionError`)
- деление на ноль (`DividedNumberError`)
- неизвестная единица (`UnknownUnitError`)
- несовместимые единицы (`IncompatibleUnitsError`)
- неверное числовое значение (`InvalidNumberError`)
- температура ниже абсолютного нуля (`UnderZeroError`)

## Команды проверки

```bash
python -m pytest
ruff check .
python -m toolkit --help
```

Тесты: 30 штук, из них вычислительное ядро проверяется напрямую (`tests/test_errors.py`), а CLI — через реальный запуск процесса (`tests/test_cli.py`).

## Структура проекта

```text
lab_01/
├── pyproject.toml
├── pytest.ini
├── README.md
├── src/
│   └── toolkit/
│       ├── __init__.py      # инициализация пакета
│       ├── __main__.py      # CLI (командная строка)
│       ├── calculator.py    # ядро калькулятора
│       ├── converter.py     # конвертер
│       ├── validator.py     # валидация токенов и единиц
│       └── errors.py        # кастомные классы ошибок
└── tests/
    ├── test_errors.py       # тесты ядра (без subprocess)
    └── test_cli.py          # тесты CLI (через subprocess)
```

## Технологии

- Python 3.9+
- setuptools (editable-установка через `pyproject.toml`)
- Алгоритм сортировочной станции (shunting-yard) для перевода в ОПЗ
- pytest (тесты)
- ruff (линтер)

## Автор

[Еваленко Екатерина Евгеньевна], [М8О-104БВ-26]
