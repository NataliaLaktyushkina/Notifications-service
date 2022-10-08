# Проектная работа 10 спринта

[Репозиторий notifications_sprint_1 (проектная работа 10-го спринта)](https://github.com/NataliaLaktyushkina/notifications_sprint_1)

Схема сервиса:

![scheme](/scheme/Notification_service.jpeg)


Запуск базы данных из папки **MongoDB**:

`docker compose up`

Шаблоны для отправки писем хранятся в MongoDB в формате:
DB - ugc_db
collection - bookmarks
documents = {user_id: [movie_id_1, movie_id_2]}

**Запуск API & Consumers:**

`docker compose up` из корня проекта

**Переменные окружения**

[Docker RabbitMQ](/.env.example)

API:

[Fast API](/fast_api/src/core/.env.example)

Workers:

[email](/workers/src/settings/email/.env.example)

[rabbitmq](/workers/src/settings/rabbitmq/.env.example)

###API для приёма событий по созданию уведомлений: ###
Принимает события от планировщика и сервисов, генерирующих события (UGC, Auth), кладет их в RabbitMQ.

- Приветственное письмо на */api/v1/user_registration*:

{
   "user_id": "0993f954-606c-4631-84f2-803f37574d08",
}

### CI / CD ###
[Workflow](.github/workflows/python.yml)
