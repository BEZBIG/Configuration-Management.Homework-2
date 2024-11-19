import requests
import xml.etree.ElementTree as ET


# Функция для парсинга POM файла и извлечения зависимостей с учетом пространства имен
def get_dependencies(group_id, artifact_id, version, depth, current_depth=0, visited=None):
    if visited is None:
        visited = set()

    # Ограничиваем максимальную глубину рекурсии
    if current_depth >= depth:
        return []

    # Собираем URL для получения POM файла
    url = f"https://repo1.maven.org/maven2/{group_id.replace('.', '/')}/{artifact_id}/{version}/{artifact_id}-{version}.pom"

    # Если пакет уже был посещен, избегаем зацикливания
    if (group_id, artifact_id, version) in visited:
        return []

    visited.add((group_id, artifact_id, version))

    # Запрос на POM файл
    try:
        response = requests.get(url)
        response.raise_for_status()  # Генерация исключения для неуспешных HTTP-статусов
    except requests.RequestException as e:
        print(f"Ошибка при загрузке POM для {group_id}:{artifact_id}:{version}. Ошибка: {e}")
        return []

    # Парсим XML с учетом пространства имен
    try:
        root = ET.fromstring(response.text)
    except ET.ParseError as e:
        print(f"Ошибка парсинга POM для {group_id}:{artifact_id}:{version}. Ошибка: {e}")
        return []

    # Пространство имен, указанное в POM файле
    namespaces = {'maven': 'http://maven.apache.org/POM/4.0.0'}

    # Ищем зависимости с учетом пространства имен
    dependencies = []
    for dependency in root.findall('.//maven:dependencies/maven:dependency', namespaces):
        dep_group_id = dependency.find('maven:groupId', namespaces).text
        dep_artifact_id = dependency.find('maven:artifactId', namespaces).text
        dep_version = dependency.find('maven:version', namespaces).text
        dependencies.append((dep_group_id, dep_artifact_id, dep_version))

    # Рекурсивный вызов для транзитивных зависимостей
    result = []
    for dep_group_id, dep_artifact_id, dep_version in dependencies:
        result.append((artifact_id, dep_artifact_id, dep_version))  # Добавляем зависимость с версией в граф
        result.extend(get_dependencies(dep_group_id, dep_artifact_id, dep_version, depth, current_depth + 1, visited))

    return result
