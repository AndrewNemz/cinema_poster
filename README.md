# Технологии

+ Python 3.7
+ Django 3.2
+ DRF
+ RESTApi
+ Djoser
+ SQLite

# Описание проекта Cinema_poster

  Пет-проект cinema_poster - киноафиша. В базе данных проекта могут храниться списки кинотеатров, 
фильмов, жанров и тэгов. 
  База данных может быть пополена только Администратором. У обычных зарегестрированных пользователей есть возможность 
добавлять фильмы в избранное и ставить рейтинги фильмам. У незарегестрированных пользователей есть возможность просматривать 
списки киноетатров и фильмов.

Пользователи могут зарегестрироваться на платформе при помощи e-mail.

# Техническое описание проекта

### Пользовательские роли

+ Аноним — может просматривать список кинотеатров и фильмов
+ Аутентифицированный пользователь (user) — помимо прав Анонимного пользователя, может добавлять фильмы в избранное и ставить оценку фильму (целое число от 1 до 10)
+ Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать.
+ Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять кинотеатры, фильмы или жанры. Может назначать роли пользователям.
+ Суперюзер Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

### Ресурсы Cinema_poster

+ Ресурс auth: аутентификация.
+ Ресурс users: пользователи.
+ Ресурс tags: Тэги для фильмов, имеющие смысл возрастоного ограничения.
+ Ресурс genres: Жанры для фильмов.
+ Ресурс cinemas: Кинотеатры.
+ Ресурс movies: Фильмы. Один фильм может показываться в нескольких кинотеатрах. Имеет один тэг(16+), но может иметь несколько жанров (приключение, фантастика).

# Как запустить проект:
### Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/AndrewNemz/cinema_poster.git

cd cinema_poster
```

### Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

### Для *nix-систем:

```
source venv/bin/activate
```

### Для windows-систем:

```
source venv/Scripts/activate
```

### Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Выполнить миграции:

```
cd cinema_poster
python3 manage.py migrate
```

### Создать суперпользователя (для раздачи прав админам):

```
python manage.py createsuperuser
```

### Запустить проект:

```
python manage.py runserver
```

### Сам проект и админ-панель искать по адресам:

```
http://127.0.0.1:8000

http://127.0.0.1:8000/admin
```

# Примеры запросов:

### Регистрация нового пользователя

#### url:
```
http://127.0.0.1:8000/api/users/
```
POST запрос
```json
 {
    "username": "test user",
    "first_name": "test_name",
    "last_name": "test last_name",
    "password": "test password",
    "email": "test@mail.ru"
}
```

ответ JSON:

```json
{
    "email": "test@mail.ru",
    "id": 4,
    "username": "test user",
    "first_name": "test_name",
    "last_name": "test last_name"
}
```

### Получение токена авторизации

#### url:
```
http://127.0.0.1:8000/api/users/
```
POST запрос
```json
{
    "email": "test@mail.ru",
    "username": "test user"
}
```

ответ JSON:

```json
{
  "auth_token": "string"
}

```

### Получение тэгов (доступно, если user.is_staff=True)

#### url:
```
http://127.0.0.1:8000/api/tags/
```

JSON в GET запросе:

```json
    {
        "id": 1,
        "name": "18+",
        "color": "#DC143C",
        "slug": "18"
    }
```

### Получение жанров (доступно, если user.is_staff=True)

#### url:
```
http://127.0.0.1:8000/api/genres/
```

Ответ JSON:
```json
    {
        "id": 5,
        "name": "Ужасы"
    }
```

### Получение списка кинотеатров

#### url:
```
http://127.0.0.1:8000/api/cinemas/
```

Ответ JSON:
```json
    {
            "id": 2,
            "name": "Rodina",
            "adress": "str, 4",
            "movies": [
                {
                    "id": 5,
                    "name": "test film 1"
                }
            ],
            "web_site": "http://www.rodina.ru"
        },
        {
            "id": 1,
            "name": "Art holl",
            "adress": "street 6, dom 5",
            "movies": [
                {
                    "id": 6,
                    "name": "test film 3"
                },
                {
                    "id": 5,
                    "name": "test film 1"
                }
            ],
            "web_site": "https://www.cinemaart.com"
        }
```

### Добавление кинотеатра (доступно, если user.is_staff=True)

#### url:
```
http://127.0.0.1:8000/api/cinemas/
```

POST запрос:
```json
        {
            "name": "cinema test",
            "adress": "dom 5",
            "movies": [
                {
                    "id": 6,
                    "name": "test film 3"
                }
            ],
            "web_site": "https://www.cinematest.com"
        }
```

Ответ JSON:
```json
{
    "id": 43,
    "name": "cinema test",
    "adress": "dom 5",
    "movies": [
        {
            "id": 6,
            "name": "test film 3"
        }
    ],


    "web_site": "https://www.cinematest.com"
}
```

### Получение списка фильмов

#### url:
```
http://127.0.0.1:8000/api/movies/
```

Ответ JSON:
```json
        {
            "id": 6,
            "name": "test film 3",
            "author": "Someone",
            "actors": "ya ti on ona",
            "genre": [
                "Биография",
                "Вестерн"
            ],
            "tag": "18+",
            "rating": {
                "rating__avg": 10.0
            },
            "is_favorite": true
        },
        {
            "id": 5,
            "name": "test film 1",
            "author": "Someone",
            "actors": "ya ti on ona",
            "genre": [
                "Биография",
                "Вестерн"
            ],
            "tag": "18+",
            "rating": {
                "rating__avg": 6.0
            },
            "is_favorite": false
        }
```

### Добавление оценки фильму

#### url:
```
http://127.0.0.1:8000/api/movies/<movie_id>/rating/
```

POST запрос

```json
{
      "movie": 6,
      "rating": 10
}

```

Ответ JSON:
```json
{
    "id": 7,
    "movie": "test film 3",
    "user": "andy",
    "rating": 10
}
```

### Получение всех оценок пользователей для конкретного фильма

#### url:

GET запрос

```
http://127.0.0.1:8000/api/movies/<movie_id>/rating/
```

Ответ JSON:
```json
        {
            "id": 3,
            "movie": "test film 3",
            "user": "admin",
            "rating": 10
        },
        {
            "id": 7,
            "movie": "test film 3",
            "user": "andy",
            "rating": 10
        }
```

### Добавление избранных фильмов POST запросом (доступно для зарегестрированных пользователей)

#### url:

POST запрос

```
http://127.0.0.1:8000/api/movies/<movie_id>/favorite/
```

Ответ JSON:
```json
{
    "id": 9,
    "user": "andy",
    "movie": "test film 3"
}
```

### Получение всех избранных пользователем фильмов (доступно для зарегестрированных пользователей)

#### url:

GET запрос

```
http://127.0.0.1:8000/api/movies/?is_favorite=1
```

Ответ JSON:
```json
        {
            "id": 6,
            "name": "test film 3",
            "author": "Someone",
            "actors": "ya ti on ona",
            "genre": [
                "Биография",
                "Вестерн"
            ],
            "tag": "18+",
            "rating": {
                "rating__avg": 10.0
            },
            "is_favorite": true
        }
```
