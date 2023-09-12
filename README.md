# TGbot_template
template for aiogram bot with postgres via async peewee


### Предварительная настройка сервера:
1. пуш в мастер самые последние изменения в ветке
2. [настройка гита на сервере](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key)
3. клон репо на сервер
4. установка docker, docker-compose
5. в папке проекта прописываем переменные окружения в .env файл (образец в файле template.env)

### Деплой:
- на сервере команда ```./spam_bot_deploy.sh```

### Как подключиться к базе из менеджера баз данных
- docker ps
- docker exec -ti <CONTAINER ID> /bin/sh
- psql -h ```<.env/POSTGRES_HOST>``` -p 5431 -U ```<.env/POSTGRES_USER>```
  - ```psql -h db -p 5432 -U spam_bot_user -d spam_bot_db``` для подключения внутри контейнера
- В ответ будет вывод ```psql: error: could not connect to server: Connection refused
        Is the server running on host "<.env/POSTGRES_HOST>" <IP ADDRESS> and accepting
        TCP/IP connections on port 5431?```
- Адрес хоста внутри контейнера будет ```<IP ADDRESS>```. При подключении надо использовать 5432 порт

### Переезд на другой сервер
1. Настроить докер
2. [Перенести базу](https://simplebackups.com/blog/docker-postgres-backup-restore-guide-with-examples/)