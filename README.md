# WildBerries Data Engineer Test Task

## Запуск сервиса

`.env`:

```bash
DATABASE_URL=sqlite:///mfd.db?check_same_thread=False
```

- `make parse` - парсинг данных и загрузка в `sqlite` таблицу `mfd.db`
- `make up` - поднятие сервиса на `fastapi`
- `make docker` - поднятие сервиса в `docker`-контейнере (если расскоментить, то можно поднять отдельно парсер)
- `make venv` - Создание виртуального окружения:
- `make format` - запуск форматтеров кода:

- TODO: `make test` - проверка работоспособности тестов (сделаю завтра)
- TODO `make lint` - запуск линтеров (сделаю завтра)

## API Reference

- `localhost:8000/docs` - документация `swagger`

## Scraped data

Посмотреть количество данных по каждой из тем статьи можно таким образом:

```sqlite
SELECT p.topic_id, t.topic_name, COUNT(p.topic_id) amount
FROM posts p
JOIN topics t on t.topic_id = p.topic_id
GROUP BY p.topic_id
ORDER BY 3 DESC;
```