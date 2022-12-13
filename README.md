Service allow to send email message after user registration and create a new email with user's text.

**Схема сервиса:**

![scheme](/scheme/Notification_scheme.png)


**Запуск API & Workers:**

`docker compose up` из корня проекта

**Alembic:**

Необходимо запустить в папке с файлом *"alembic.ini":*

`alembic revision -m "initial"`

`alembic upgrade head`

`alembic revision --autogenerate -m "create_tables"`

`alembic upgrade head`

**Переменные окружения**

[Docker RabbitMQ](/.env.example)

API:

[Fast API](/fast_api/src/core/.env.example)

[Admin_API](admin_api/src/core/.env.example)

Workers:

[email](/workers/src/settings/email/.env.example)

[rabbitmq](/workers/src/settings/rabbitmq/.env.example)

[postgres](/workers/src/settings/postgres/.env.example)

[common](/workers/src/settings/common/.env.example)

### Формат payload:
```python
payload = [{'users': ['user_id_1'],
            'content':
               {'movie': 1, 'movie_2': 1}
            },
            {'users': ['user_id_2'],
            'content':
               {'movie': 2, 'movie_2': 2}
            }]
```

### Приветственное письмо после регистрации пользователя:

**API**:

*127.0.0.1:81/api/openapi*


- Регистрация пользователя */api/v1/user_registration*:

{
   "user_id": "0993f954-606c-4631-84f2-803f37574d08",
}

API кладет сообщение в очередь (RabbitMQ),
далее consumer в реальном времени читает очередь и отправляет письмо пользователю

[Auth service](https://github.com/NataliaLaktyushkina/Auth_sprint_2)

### Периодические события:
[Events generator](workers/src/events_generator/generator.py)


### Admin panel:
**API**:

*http://127.0.0.1:81/adminapi/openapi*

### CI / CD:
[Workflow](.github/workflows/python.yml)
