# Проектная работа 10 спринта

[Репозиторий notifications_sprint_1 (проектная работа 10-го спринта)](https://github.com/NataliaLaktyushkina/notifications_sprint_1)

Схема сервиса:

![scheme](/scheme/Notification_service.jpeg)


Запуск базы данных из папки **MongoDB**:

`docker compose up`

###API для приёма событий по созданию уведомлений: ###
Принимает события от планировщика и сервисов, генерирующих события (UGC, Auth), кладет их в RabbitMQ.

- Приветственное письмо на */api/v1/user_registration*:

{
   "user_id": "0993f954-606c-4631-84f2-803f37574d08",
}

### CI / CD ###
[Workflow](.github/workflows/python.yml)
