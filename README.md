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