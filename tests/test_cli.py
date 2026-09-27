import subprocess
import sys
from pathlib import Path

def test_cli_calc():
    """
    Проверяет вычисление арифметического выражения через CLI.

    Запускает программу toolkit с командой calc и выражением
    2+7*2, после чего проверяет код завершения программы
    и полученный результат.

    Команды:
        calc: команда для вычисления выражения.
        2+7*2: арифметическое выражение, передаваемое программе.

    Параметры subprocess.run:
        capture_output: сохраняет стандартный вывод и вывод ошибок
            для последующей проверки.
        text: возвращает stdout и stderr в виде строк.
        cwd: задаёт папку src в качестве рабочей директории.

    Проверки:
        returncode == 0: программа завершилась без ошибки.
        stdout == "16": программа вернула правильный результат.
    """
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "calc", "2+7*2"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent / "src"
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "16"


def test_cli_convert():
    """
    Проверяет конвертацию единиц измерения через CLI.

    Запускает программу toolkit с командой convert и проверяет,
    что значение 100 сантиметров правильно переводится в метры.

    Команды:
        convert: команда для конвертации значения.
        100: исходное значение.
        --from cm: исходная единица измерения — сантиметры.
        --to m: целевая единица измерения — метры.

    Параметры subprocess.run:
        capture_output: сохраняет stdout и stderr.
        text: возвращает результаты выполнения в виде строк.
        cwd: задаёт директорию src как рабочую директорию.

    Проверки:
        returncode == 0: команда выполнена успешно.
        stdout == "1.0": результат конвертации правильный.
    """
    result = subprocess.run(
        [sys.executable,
         "-m",
         "toolkit",
         "convert",
         "100",
         "--from",
         "cm",
         "--to",
         "m"
         ],
         capture_output=True,
         text=True,
         cwd=Path(__file__).parent.parent / "src"
    )
    assert result.returncode == 0
    assert result.stdout.strip()=="1.0"


def test_cli_invalid_character():
    """
    Проверяет обработку выражения с недопустимым символом через CLI.

    Запускает команду calc с выражением 2@7, содержащим символ @,
    который не поддерживается калькулятором.

    Команды:
        calc: команда для вычисления выражения.
        2@17: некорректное арифметическое выражение.

    Параметры subprocess.run:
        capture_output: сохраняет stdout и stderr для проверки ошибки.
        text: возвращает вывод программы в виде строк.
        cwd: задаёт директорию src как рабочую директорию.

    Проверки:
        returncode == 2: программа завершилась с кодом ошибки.
        stderr != "": программа вывела сообщение об ошибке.
    """
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "calc", "2@17"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent / "src"
    )

    assert result.returncode == 2
    assert result.stderr.strip() != ""