import pytest
import requests
from unittest.mock import patch, MagicMock
from main import get_dependencies, generate_dot_code  # Замените `your_script` на имя вашего файла

# Тест для базового случая с одной зависимостью
@patch("main.requests.get")
def test_get_dependencies_basic(mock_get):
    # Подготовка mock-ответа для POM файла
    mock_response = """<?xml version="1.0"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0">
        <dependencies>
            <dependency>
                <groupId>com.example</groupId>
                <artifactId>example-artifact</artifactId>
                <version>1.0.0</version>
            </dependency>
        </dependencies>
    </project>
    """
    mock_get.return_value = MagicMock(status_code=200, text=mock_response)

    # Проверяем, что зависимость извлекается корректно
    dependencies = get_dependencies("org.test", "test-artifact", "1.0.0", 1)
    assert dependencies == [("test-artifact", "example-artifact", "1.0.0")]


# Тест для рекурсивного случая с транзитивными зависимостями
@patch("main.requests.get")
def test_get_dependencies_recursive(mock_get):
    # Подготовка mock-ответов для рекурсивных зависимостей
    mock_response_main = """<?xml version="1.0"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0">
        <dependencies>
            <dependency>
                <groupId>com.example</groupId>
                <artifactId>example-artifact</artifactId>
                <version>1.0.0</version>
            </dependency>
        </dependencies>
    </project>
    """
    mock_response_dependency = """<?xml version="1.0"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0">
        <dependencies>
            <dependency>
                <groupId>com.sub.example</groupId>
                <artifactId>sub-example-artifact</artifactId>
                <version>2.0.0</version>
            </dependency>
        </dependencies>
    </project>
    """
    # Настраиваем последовательность вызовов mock
    mock_get.side_effect = [
        MagicMock(status_code=200, text=mock_response_main),
        MagicMock(status_code=200, text=mock_response_dependency),
    ]

    # Проверяем рекурсивное извлечение
    dependencies = get_dependencies("org.test", "test-artifact", "1.0.0", 2)
    assert dependencies == [
        ("test-artifact", "example-artifact", "1.0.0"),
        ("example-artifact", "sub-example-artifact", "2.0.0"),
    ]


# Тест на обработку ошибки HTTP-запроса
@patch("main.requests.get")
def test_get_dependencies_with_error(mock_get):
    # Эмулируем ошибку HTTP-запроса
    mock_get.side_effect = requests.RequestException("HTTP Error")

    dependencies = get_dependencies("org.test", "test-artifact", "1.0.0", 1)
    assert dependencies == []  # Ожидаем пустой список при ошибке


# Тесты для generate_dot_code
def test_generate_dot_code_basic():
    dependencies = [("artifact1", "artifact2", "1.0")]
    dot_code = generate_dot_code(dependencies)
    expected_dot_code = """digraph G {
    "artifact1" -> "artifact2" [label="1.0"];
}
"""
    assert dot_code == expected_dot_code


def test_generate_dot_code_empty():
    dependencies = []
    dot_code = generate_dot_code(dependencies)
    expected_dot_code = """digraph G {
}
"""
    assert dot_code == expected_dot_code


def test_generate_dot_code_multiple_dependencies():
    dependencies = [
        ("artifact1", "artifact2", "1.0"),
        ("artifact2", "artifact3", "2.0"),
    ]
    dot_code = generate_dot_code(dependencies)
    expected_dot_code = """digraph G {
    "artifact1" -> "artifact2" [label="1.0"];
    "artifact2" -> "artifact3" [label="2.0"];
}
"""
    assert dot_code == expected_dot_code
