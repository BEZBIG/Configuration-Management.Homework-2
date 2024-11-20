Разработать инструмент командной строки для визуализации графа
зависимостей, включая транзитивные зависимости. Сторонние средства для
получения зависимостей использовать нельзя.


Зависимости определяются по имени пакета языка Java (Maven). Для
описания графа зависимостей используется представление Graphviz.
Визуализатор должен выводить результат на экран в виде кода.


Ключами командной строки задаются:


• Путь к программе для визуализации графов.


• Имя анализируемого пакета.


• Путь к файлу-результату в виде кода.


• Максимальная глубина анализа зависимостей.


Все функции визуализатора зависимостей должны быть покрыты тестами.

Структура файлов в проекте:


config.xml - Конфигурационный файл, содержит 2 параметра(hostname, filesystem)


main.py - Главный файл программы, в котором мы парсим зависимости из POM-файла и создаем описание графа зависимостей, используя представление Graphviz.


test.py - Файл программы, который тестирует работоспособность всей программы.


dependencies.dot - Файл, в который сохраняется описание графа зависимостей


Пример скрипта для запуска программы: python main.py org.springframework.boot:spring-boot-starter-web:2.5.6 --depth 2 --output dependencies.dot


Работа с инструментом командной строки для визуализации графа зависимостей:

![Image alt1](https://github.com/BEZBIG/Configuration-Management.Homework-2/blob/master/pic/1.png)

Содержимое файла dependencies.dot:

![Image alt2](https://github.com/BEZBIG/Configuration-Management.Homework-2/blob/master/pic/2.png)

Проверка работоспособности инструмента командной строки для визуализации графа зависимостей с помощью сайта для построения графов: 

![Image alt3](https://github.com/BEZBIG/Configuration-Management.Homework-2/blob/master/pic/3.png)

Тесты программы: 

![Image alt4](https://github.com/BEZBIG/Configuration-Management.Homework-2/blob/master/pic/4.png)

![Image alt5](https://github.com/BEZBIG/Configuration-Management.Homework-2/blob/master/pic/5.png)
![Image alt6](https://github.com/BEZBIG/Configuration-Management.Homework-2/blob/master/pic/5.2.png)

![Image alt7](https://github.com/BEZBIG/Configuration-Management.Homework-2/blob/master/pic/6.png)

![Image alt8](https://github.com/BEZBIG/Configuration-Management.Homework-2/blob/master/pic/7.png)

![Image alt9](https://github.com/BEZBIG/Configuration-Management.Homework-2/blob/master/pic/8.png)

![Image alt10](https://github.com/BEZBIG/Configuration-Management.Homework-2/blob/master/pic/9.png)

Оперируем с тестовым файлом и проводим проверку:

![Image alt11](https://github.com/BEZBIG/Configuration-Management.Homework-2/blob/master/pic/10.png)
