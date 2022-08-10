# Запуск проекта
1. При возникновении ошибки: \
`./psycopg/psycopg.h:35:10: fatal error: Python.h: Файл не существует`

Неободимо ([ссылка на решение](https://www.codegrepper.com/code-examples/python/.%2Fpsycopg%2Fpsycopg.h%3A35%3A10%3A+fatal+error%3A+Python.h%3A+No+such+file+or+directory)):

`sudo apt-get install python3-dev` 

2. Подключение docker-образа для создания в нем БД: \
`docker run --name advertisement_postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres` \
\
**Решение проблем**\
При возникновении ошибки о недостаточности прав доступа запуска docker: 
    > docker: Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Post " ... "  : dial unix /var/run/docker.sock: connect: permission denied. <br>

    Необходимо ввести команду:<br>
    `sudo usermod -a -G docker $USER`<br>
    To apply the new group membership, log out of the server and back in, or type the following:<br>
    `su - ${USER}`<br>
3. Узнать ID созданного docker-образа:<br>
    `docker ps`<br>
4. Запуск данного docker-образа:<br>
    `docker start <ID>`
5. Накатываем миграции:<br>
    `./manage.py makemigrations`<br>
    `./manage.py migrate`

# Критерии выполнения:

- [ ]  Работа с пользователями реализованая через GenericView из DRF - ListApiView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
- [ ]  При выводе списка пользователей используется встроенная пагинация DRF
- [ ]  API для модели Location реализовано с использованием ViewSet и Router
- [ ]  В проекте используются Serializers
- [ ]  Все фильтры выполнены с использованием lookup's
- [ ]  Типы данных в JSON отдаются корректно
- [ ]  Методы из спецификации работают
# Проверка ДЗ
Для проверки удобно использовать postman-запросы. Поэтому прикрепил файл в корень прокта ["HW29.postman_collection.json"](HW29.postman_collection.json), который можно импортировать в postman.\
Инициализация БД в том порядке, в котором они расположены в postman списке: 
  + локации, 
  + категории, 
  + пользователи,
  + объявления.
<br><br>

**createsuperuser**
  + login: django
  + password: django