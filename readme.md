# Сервис генерации короткой ссылки

- Создание короткой ссылки (на вход передаём полный url, в ответ получаем короткий url)
- Удаление ссылки (на вход ранее сгенерированный короткий url, ответ статус операции)
- Получение полного url (на вход короткий url, в ответ полный url)

Пример полного url - https://music.yandex.ru/album/5307396/track/38633706  
Пример короткого url - [const.com/A8z1](http://const.com/A8z1)

## deploy

### build and run

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml build
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

or you can add a path variable

```bash
export PATH="./.bin:$PATH"
```

and then

```bash
dev build && dev up
```

### run migrations

run inside server container

```bash
alembic upgrade head
```
