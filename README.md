# Проектная работа 10 спринта

[Репозиторий notifications_sprint_1 (проектная работа 10-го спринта)](https://github.com/NataliaLaktyushkina/notifications_sprint_1)

Схема сервиса:

![scheme](/scheme/Notification_scheme.png)


Запуск базы данных из папки **MongoDB**:

`docker compose up`

**Запуск API & Workers:**

`docker compose up` из корня проекта

**Переменные окружения**

[Docker RabbitMQ](/.env.example)

API:

[Fast API](/fast_api/src/core/.env.example)

Workers:

[email](/workers/src/settings/email/.env.example)

[rabbitmq](/workers/src/settings/rabbitmq/.env.example)

###Приветственное письмо после регистрации пользователя: ###
API -> Queue -> Worker -> Email

**API** *127.0.0.1:81/api/openapi*

- Регистрация пользователя */api/v1/user_registration*:

{
   "user_id": "0993f954-606c-4631-84f2-803f37574d08",
}

API кладет сообщение в очередь (RabbitMQ),
далее consumer в реальном времени читает очередь и отправляет письмо пользователю

[Auth service](https://github.com/NataliaLaktyushkina/Auth_sprint_2)

###Периодические события: ###
[Events generator](workers/src/events_generator/generator.py)


###Admin panel: ###


### CI / CD: ###
[Workflow](.github/workflows/python.yml)
