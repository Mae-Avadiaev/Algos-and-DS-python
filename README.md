### Python experience in OOP, algorithms and data structures 

## 1. Yandex contest 
for Yandex Academy for school of Back-end development

## 2. Advanced Algorithms and Complexity 
is the 5th and most exiting part of the **Algorithms and Data Structures Course** provided by **University of San Diego and HSE**. 
*Comments are included in the files.*

## 3. REST API сервис

Задача: спроектировать и разработать API для системы опросов пользователей.

Функционал для администратора системы:
- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

Функционал для пользователей системы:
- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

Инструкции по развертыванию:
- cd папка_с_проектом
- docker-compose up --build
- Откройте новое окно терминала и наберите следующие команды
- docker exec -ti test_task_web_1 /bin/sh
- python manage.py migrate
- python manage.py createsuperuser
- (enter)
- введите пароль (root)
- повторите пароль (root)
- y

Документация API:
- GET /poll_app/{user_id} - список доступных опросов для {user_id}
- GET /poll_app/{user_id}/vote/ - список вопросов опроса
- POST /poll_app/{user_id}/vote/submit/ - проголосовать 
- GET /poll_app/{user_id}/results/ - посмотреть результаты опроса
- GET /poll_app/{user_id}/results_main/ - список результатов для {user_id}
- GET /admin/ - админка

Что не получилось реализовать:
- Скрипт автоматического запуска миграций и добавления суперюзера
- Подключить автодокументацию Swagger (No operations defined in spec!)
