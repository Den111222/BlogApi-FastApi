# BlogApi-FastApi
ТЗ

1. Сделать Блог со следующими сущностями:
- Posts
- Categories
- Tags
- Authors
2. Сделать структуру базы данных для этих сущностей и описать модели.
- Подключить Swagger UI
- Сделать CRUD для запросов

Решение

1. Сделан Блог с сущностями:
- Posts
- Categories
- Tags
- Authors - как отдельная сущность не сделана, требует доработки (для чего нужна данная сущность)

2. Cтруктура базы данных для этих сущностей описана моделиью в [database.puml](documentation%2Fdatabase.puml)
- Подключен Swagger UI для `http://127.0.0.1:8080/blog/api/openapi#/`
- Сделан CRUD для всех запросов

3. Сделан сервис Авторизации c сущностями:
- Users
- Tokens
- Подключен Swagger UI для `http://127.0.0.1:8001/auth/api/openapi#/`

4. Запуск `docker-compose up -d`

# BlogApi-FastApi

## Technical Specification

1. Create a Blog with the following entities:
   - Posts
   - Categories
   - Tags
   - Authors
2. Design the database structure for these entities and describe the models.
   - Integrate Swagger UI
   - Implement CRUD operations for the requests

## Solution

1. The Blog has been created with the following entities:
   - Posts
   - Categories
   - Tags
   - Authors - not implemented as a separate entity, requires further development (clarification needed on the purpose of this entity)

2. The database structure for these entities is described in the model [database.puml](documentation%2Fdatabase.puml).
   - Swagger UI is integrated and accessible at `http://127.0.0.1:8080/blog/api/openapi#/`
   - CRUD operations for all requests are implemented

3. An Authorization service has been created with the following entities:
   - Users
   - Tokens
   - Swagger UI is integrated and accessible at `http://127.0.0.1:8001/auth/api/openapi#/`

4. To start, run:
   ```sh
   docker-compose up -d
