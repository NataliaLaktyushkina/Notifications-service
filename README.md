# Проектная работа 10 спринта

[Репозиторий notifications_sprint_1 (проектная работа 10-го спринта)](https://github.com/NataliaLaktyushkina/notifications_sprint_1)

Схема сервиса:

![scheme](/scheme/Notification_service.jpeg)


Запуск базы данных из папки **MongoDB**:

`docker compose up`

**Запуск API & Consumers:**

`docker compose up` из корня проекта

**Переменные окружения**

[Docker RabbitMQ](/.env.example)

API:

[Fast API](/fast_api/src/core/.env.example)

Workers:

[email](/workers/src/settings/email/.env.example)

[rabbitmq](/workers/src/settings/rabbitmq/.env.example)

###API ###
*127.0.0.1:80/api/openapi*

- Регистрация пользователя */api/v1/user_registration*:

{
   "user_id": "0993f954-606c-4631-84f2-803f37574d08",
}

API кладет сообщение в очередь (RabbitMQ),
далее consumer в реальном времени читает очередь и отправляет письмо пользователю

### CI / CD ###
[Workflow](.github/workflows/python.yml)
